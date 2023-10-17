#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# This is for Linux devices that don't have an NVIDIA GPU, E.g., an Intel NUC

import os
import json
import time
import gc
import logging
import sys
from linuxDataCPU import LinuxCpuData

# this allows us to import modules, classes, scripts et al from the
# "common" directory. This will get flagged by most linters, but it's
# unavoidable as you can't run this code before you import the os library
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
print(sys.path)

from common.deviceTools import DeviceUtilities

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataLinuxCPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client, getData, topic):

    while True:

        time.sleep(1)

        # get CPU utilization
        cpuUtil = getData.getCPUData()

        # get current RAM use
        ramUse = getData.getRamData()

        # get current freq and core count
        cpuFreq, coreCount = getData.getFreq()

        # get CPU temperature
        cpuTemp = getData.coreTemp()

        payload = {
                   "cpuTemp": cpuTemp,
                   "cpuFreq": cpuFreq,
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

        del payload, cpuUtil, ramUse, cpuFreq, cpuTemp, status, result
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
