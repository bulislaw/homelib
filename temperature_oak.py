#!/usr/bin/env python

from spyrk import SparkCloud

class TemperatureOak(SparkCloud):
    def __init__(self, devf=".temperature.oak"):
        with open(devf) as f:
            self.name, self.token = f.readline()[:-1].split(":")

            SparkCloud.__init__(self, self.token)

    def read_temp(self):
        return self.devices[self.name].temp_up

    def read_hum(self):
        return self.devices[self.name].hum_up

if __name__ == "__main__":
    oak = TemperatureOak()
    print(oak.read_temp())
    print(oak.read_hum())
