#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# this would be for linux devices where I'm not using an NVIDIA GPU/a GPU
# at all, e.g.single board computers running headless, or devices like an
# Intel NUC so I would only monitor the CPU

import json
import time
import gc
import os
import logging
import sys
from linuxDataGPU import LinuxGPUSensors
from linuxDataCPU import LinuxCpuData

# this allows us to import modules, classes, scripts et al from the
# "common" directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities

logging.basicConfig(filename='hardwareDataLinuxGPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client, getData, getGpuData, topic):

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

        # get GPU Data
        temp, gpuLoad, gpuVram, gpuPower, gpuClock = getGpuData.gpuQuery()

        # build payload
        payload = {
                   "cpuTemp": cpuTemp,
                   "cpuFreq": cpuFreq,
                   "cpuUse": cpuUtil,
                   "ramUse": ramUse,
                   "gpuTemp": temp,
                   "gpuLoad": gpuLoad,
                   "gpuVram": gpuVram,
                   "gpuPower": gpuPower,
                   "gpuClock": gpuClock
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

    # load config file(s)
    broker, port, topic, user, pwd = deviceUtilities.loadConfigs(configFile,
                                                                 secrets)

    # get unique client ID
    clientID = deviceUtilities.getClientID()

    # get mqtt client
    client, code = deviceUtilities.mqttClient(clientID, user, pwd, broker,
                                              port)

    # instantiate CPU data class & utilities class
    getGpuData = LinuxGPUSensors()
    getData = LinuxCpuData()

    # start monitoring
    try:
        monitor(client, getData, getGpuData, topic)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
