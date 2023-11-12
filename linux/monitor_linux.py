#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# This is for Linux devices that don't have an NVIDIA GPU, E.g., an Intel NUC
# CLI instructions monitor_linux.py <MQTT topic name as a string>

import os
import json
import time
import gc
import logging
import sys
from linux_cpu_data import LinuxCpuData

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities  # noqa: E402

# create logger for logging errors, exceptions and the like
logging.basicConfig(filename='hardwareDataLinuxCPU.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client: object, getData: object, topic: str):

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

        if status != 0:
            print(f'Failed to send {payload} to: {topic}')
            logging.debug(f'MQTT publishing failure, return code: {status}')

        del payload, cpuUtil, ramUse, cpuFreq, cpuTemp, status, result
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

    # instantiate CPU & GPU data classes
    getData = LinuxCpuData()

    # start data monitoring
    try:
        monitor(client, getData, TOPIC)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
