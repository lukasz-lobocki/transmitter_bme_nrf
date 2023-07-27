"""XIAO_nRF52840"""
import machine
import time
import struct

import sub.lobo_bme280 as bme280
from sub.lobo_nrf24l01 import NRF24L01
from sub.pin import *


def sensor_setup():
    bme = bme280.BME280(
        mode=5,
        address=0x77,
        i2c=machine.I2C(
            I2C_PORTS[0]["ID"], sda=I2C_PORTS[0]["I2C_SDA"], scl=I2C_PORTS[0]["I2C_SCL"]
        ),
    )  # 119 = 0x77

    # Init for Warsaw
    bme.sealevel = 100300

    return bme


def transmitter_setup():
    _payload_size = 3 * 4  # 3 times 4 bytes per float

    # chip enable
    D0.init(mode=machine.Pin.OUT, value=0)
    # chip select NOT
    D1.init(mode=machine.Pin.OUT, value=1)

    # Enable SPI
    spi = machine.SPI(SPI_PORTS[0]["ID"])
    spi.init()

    # Enable nRF
    nrf = NRF24L01(spi, cs=D1, ce=D0, payload_size=_payload_size)
    nrf.reg_write(0x01, 0b11111000)  # enable auto-ack on all pipes

    # Setup piping
    pipe = b"\xf5\x26\xe3\x13\xfb"
    nrf.open_tx_pipe(pipe)

    return nrf


def read(sensor):
    reading = sensor.read_compensated_data()
    stateA = round(reading[0], 2)
    stateB = round(reading[1] / 100, 2)
    stateC = round(reading[2], 2)
    return (stateA, stateB, stateC)


def transmit(transmitter, sensor):
    stateA, stateB, stateC = read(sensor)

    # Clean the pipe and send
    transmitter.stop_listening()
    try:
        transmitter.send(struct.pack("fff", stateA, stateB, stateC))
    except OSError:
        print("message lost")
    transmitter.start_listening()

    print("\n%sC" % stateA)
    #     print("%shPa" % stateB)
    #     print("%s%%" % stateC)

    # Flash red onboard LED
    for _ in range(3):
        if machine.Pin.board.P26.value() == 1:
            machine.Pin.board.P26.low()
        else:
            machine.Pin.board.P26.high()
        time.sleep_ms(500)


def sensor_restart():
    # Dim red onboard LED
    machine.Pin.board.P26.high()

    # Restart sensor powered via D2_A2
    machine.Pin.board.D2_A2.init(mode=Pin.OUT)
    machine.Pin.board.D2_A2.low()
    machine.Pin.board.P26.low()

    time.sleep_ms(500)

    machine.Pin.board.D2_A2.high()
    machine.Pin.board.P26.high()


sensor_restart()

print("Waiting...")
for _ in range(3):  # Flash blue onboard LED
    machine.Pin.board.P6.low()
    time.sleep_ms(500)
    machine.Pin.board.P6.high()
    time.sleep_ms(500)

print("Setting up...")
transmitter = transmitter_setup()
sensor = sensor_setup()

for _ in range(3):  # Flash green onboard LED
    machine.Pin.board.P30.low()
    time.sleep_ms(500)
    machine.Pin.board.P30.high()
    time.sleep_ms(500)

print("Running...")
while True:
    transmit(transmitter=transmitter, sensor=sensor)
    time.sleep_ms(1000 * 30)
