#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# This script is specific to the Orange Pi 5 Plus with
# the Rockchip 3588 System on Chip (SOC) Running Joshua Riek's
# Ubuntu Distro for RockChip Devices:
# https://github.com/Joshua-Riek/ubuntu-rockchip


import json
import time
import gc
import os
import logging
import sys
from linuxDataCPU import LinuxCpuData

# this allows us to import modules, classes, scripts et al from the
# "common" directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataRockChip.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client, getData, topic):

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

    configFile = args[0]
    secrets = args[1]

    broker, port, topic, user, pwd = deviceUtilities.loadConfigs(configFile,
                                                                 secrets)

    # get unique client ID
    clientID = deviceUtilities.getClientID()

    # get mqtt client
    client, code = deviceUtilities.mqttClient(clientID, user, pwd, broker,
                                              port)

    # instantiate CPU data class & utilities class
    getData = LinuxCpuData()

    # start monitoring
    try:
        monitor(client, getData, topic)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
