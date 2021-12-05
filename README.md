# raspberrypi_onewire_exporter
Raspberry Pi 1-Wire protocol Prometheus exporter for DS18B20

This script finds the 1-Wire DS18B20 sensors, and exports them as a Prometheus export on port `9200`

You can launch it as a service with the file `onewire_exporter.service` on Debian/Raspbian.
