from glob import glob
import time
import random
from temp_reader import read_temp_raw
from datetime import datetime
from prometheus_client import start_http_server, Summary, Gauge
# Based on https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
# Based on https://pypi.org/project/prometheus-flask-exporter/
sensor_base_dir = "/sys/bus/w1/devices/"


if __name__ == "__main__":
    # Prometheus Server Stuffs
    REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing requests')
    start_http_server(9200)
    gauge = Gauge('temperature', 'Temperature', ['sensor_name'])

    @REQUEST_TIME.time()
    def process_request():
        """A dummy function that takes some time"""
        time.sleep(1)


    while True:
        process_request()

        print("")
        print("-" * 20)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        print(dt_string)

        ds18b20_folders = glob(sensor_base_dir + '28*')
        for folder in ds18b20_folders:
            print(folder + ": " + read_temp_raw(folder))

            gauge.labels(str(folder.replace('/sys/bus/w1/devices/', ''))).set(read_temp_raw(folder))

        print(ds18b20_folders)
        time.sleep(60)
