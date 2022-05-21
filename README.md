# Linkhub Exporter

A Prometheus exporter for Alcatel Linkhub boxes.

Tested with an Alcatel HH41 4G LTE hotspot WiFi router.

![Alcatel HH41 product info](docs/linkhub_product.jpg)

## Usage

Install Poetry for you system (need `>=1.2.0b1` currently if using
the dynamic versioning, and have to add the relevant plugin with
`poetry plugin add poetry-dynamic-versioning-plugin`). Then install the
package with:

```shell
poetry install
```

You'll need a Request Key to run exporter, which is derived from the
login password of router box admin interface. See below how to
obtain it.

Once you have a key, you can set it in multiple ways:

* In `.secrets.toml`, see the template shipped at `secrets.toml.template`
  for the format (note the `.` for the non-template filename), OR
* Set an environment variable `LINKHUB_REQUEST_KEY` with the value, e.g.
  `export LINKHUB_REQUEST_KEY=...` in your shell where `...` is replaced with
  the actual value.

Then start up the exporter:

```shell
poetry run exporter
```

### Running in Docker

Build the image with the included Dockerfile from the cloned repository,
let's say:

```shell
docker build -t linkhub_exporter
```

and then run the resulting image as:

```shell
docker run -ti --rm -e "LINKHUB_REQUEST_KEY=...." -p 9877:9877 linkhub_exporter
```

which exposes the Prometheus metrics on `http://localhost:9877`. Don't forget
to set the `LINKHUB_REQUEST_KEY` value, or add it in an `.env` file and
run things as:

```shell
docker run -ti --rm --env-file .env -p 9877:9877 linkhub_exporter
```

### Running in Docker Compose

You can add this exporter as a container in your `docker-compose.yml`, along
similar lines (other container configuration has been snip'd):

```yaml
  linkhub:
    image: imrehg/linkhub_prometheus_exporter
    restart: always
    ports:
      - "9877:9877"
    environment:
      - LINKHUB_EXPORTER_ADDRESS='0.0.0.0'
    env_file:
      - .env
```

The `LINKHUB_REQUEST_KEY` value should be set in the `.env` file (or wherever
you will keep the configuration for this particular service). You can comment
out the `ports` section if you don't want to view the results outside of the
docker compose run services. You might want to add `network` field if you
are running things within a custom network.

Finally, you probably want to set an explicit tag for the image value.

### Setting up task in Prometheus

The setup in Prometheus is pretty straightforward, using the relevant IP/port
combo. If the server is run manually or through Docker on its own, use the machine's
IP that's running it, and the port that is set in the config. If docker compose
is used, the can use the service name to connect to it automatically, say like this:

```yaml
  - job_name: 'linkhub'
    scrape_interval: 5s
    static_configs:
      - targets: ['linkhub:9877']
```

(The other parts of the Prometheus configuration are omitted.)

### Getting the request key

Currently the easiest way to get it is to:

* Open a browser  and navigate to your router admin interface
* Open the debug console, and ensure that network requests are logged there
* Log in to the admin interface
* Check requests going to `webapi`, look for the requests headers, and the
  value of the `_TclRequestVerificationKey` is what you should use for the
  request key setting of this exporter.


### Showing the metrics in Grafana

An [example Grafana dashboard](extra/Grafana_Sammple_LinkHub_Metrics.json)
setup is provided in the `extra` folder.

![Grafana dashboard screenshot part 1](docs/grafana_screenshot1.png)

![Grafana dashboard screenshot part 2](docs/grafana_screenshot2.png)

## License

Copyright 2022 Gergely Imreh <gergely@imreh.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.