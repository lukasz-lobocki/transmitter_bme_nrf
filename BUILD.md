# transmitter_bme_nrf

## Typical build workflow

```bash
git add --update
```

```bash
git commit -m "fix: change"
```

```bash
poetry run semantic-release version
```

:no_entry: There is **no need** for separate `git push`. It is done by `semantic-release`.

## Cookiecutter initiation

```bash
cookiecutter \
  ssh://git@github.com/lukasz-lobocki/py-pkgs-cookiecutter.git \
  package_name="transmitter_bme_nrf"
```

### Cookiecutter was run

#### with following variables

- package_name: **`transmitter_bme_nrf`**;
package_short_description: `Transmitting end of temperature, pressure, humidity.`

- package_version: `0.0.0`; python_version: `3.10`

- author_name: `Lukasz Lobocki`;
open_source_license: `CC0 v1.0 Universal`

- __package_slug: `transmitter_bme_nrf`; include_github_actions: `no`

#### on

`2023-07-27 15:05:13 +0200`
