#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# This script is specific to the Orange Pi 5 Plus with
# the Rockchip 3588 System on Chip (SOC) Running Joshua Riek's
# Ubuntu Distro for RockChip Devices:
# https://github.com/Joshua-Riek/ubuntu-rockchip
# CLI instructions <filename> <MQTT topic name as a string>


import json
import time
import gc
import os
import logging
import sys
from linux_cpu_data import LinuxCpuData

# this allows us to import modules, classes, scripts et al from the
# "common" directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities  # noqa:  E402

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataRockChip.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client: object, getData: object, topic: str):

    while True:

        time.sleep(1)

        # get CPU utilization
        cpuUtil = getData.getCPUData()

        # get current RAM use
        ramUse = getData.getRamData()

        # get per CPU frequencies (bigCore0, bigCore1, littleCore)
        littleCoreFreq, bigCore0Freq, bigCore1Freq = getData.\
            getRockChip3588Freqs()

        # get system temperatures
        socTemp, bigCore0Temp, bigCore1Temp, littleCoreTemp, centerTemp, \
            gpuTemp, npuTemp, nvmeTemp = getData.sysTemps()

        payload = {
            "SOC": socTemp,
            "bigCore0": bigCore0Temp,
            "bigCore1": bigCore1Temp,
            "littleCore": littleCoreTemp,
            "Center": centerTemp,
            "GPU": gpuTemp,
            "NPU": npuTemp,
            "NVME": nvmeTemp,
            "littleCoreFreq": littleCoreFreq,
            "bigCore0Freq": bigCore0Freq,
            "bigCore1Freq": bigCore1Freq,
            "cpuUse": cpuUtil,
            "ramUse": ramUse
        }

        payload = json.dumps(payload)

        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f'Data {payload} was published to: {topic}')
        else:
            print(f'Failed to send {payload} to: {topic}')
            logging.debug(f'MQTT publishing failure, return code: {status}')

        del payload, socTemp, bigCore0Temp, bigCore1Temp, \
            littleCoreTemp, centerTemp, gpuTemp, npuTemp, nvmeTemp, \
            status, result
        gc.collect()


def main():

    # instantiate utilities class
    deviceUtilities = DeviceUtilities()

    # parse command line arguments
    args = sys.argv[1:]

    TOPIC = args[0]

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    clientID = deviceUtilities.getClientID()

    # get mqtt client
    client, code = deviceUtilities.mqttClient(clientID, MQTT_USER,
                                              MQTT_SECRET, MQTT_BROKER,
                                              MQTT_PORT)

    # instantiate CPU data class & utilities class
    getData = LinuxCpuData()

    # start monitoring
    try:
        monitor(client, getData, TOPIC)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
