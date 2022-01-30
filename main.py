from glob import glob
import time
import random
from temp_reader import read_temp_raw
from datetime import datetime
from prometheus_client import start_http_server, Summary, Gauge
# Based on https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/software
# Based on https://pypi.org/project/prometheus-flask-exporter/
sensor_base_dir = "/sys/bus/w1/devices/"

sensors = {
    # Examples
    #'28-00000db6fb7e': 'Front A/C',
    #'28-00000db717f0': 'Exhaust Servers',
    #'28-00000db81779': 'Exhaust Fan',
    #'28-00000db870d0': 'Front Servers',
}

if __name__ == "__main__":
    # Prometheus Server Stuffs
    REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing requests')
    start_http_server(9200)
    gauge = Gauge('temperature', 'Temperature', ['sensor_name', 'alias'])

    @REQUEST_TIME.time()
    def process_request():
        """A dummy function that takes some time"""
        time.sleep(1)


    while True:
        process_request()

        print("-" * 20)

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        print(dt_string)

        ds18b20_folders = glob(sensor_base_dir + '28*')

        print("Detected folders:")
        for folder in ds18b20_folders:
            print("- " + folder)

        print("")

        for folder in ds18b20_folders:
            temperature = read_temp_raw(folder)
            print(folder + ": " + temperature)
            sensor_name = folder.replace('/sys/bus/w1/devices/', '')
            sensor_alias = sensors[sensor_name]
            print("    Sensor: " + sensor_alias)
            print("")
            gauge.labels(sensor_name, sensor_alias).set(temperature)            

        #print(ds18b20_folders)
        time.sleep(60)
