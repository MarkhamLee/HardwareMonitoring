# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# script to retrieve Windows data and publish it to an MQTT topic
# leverages psutil + the LibreHardwareMonitor library

import json
import time
import gc
import os
import logging
import sys
from windowsdata import WindowsSensors

# this allows us to import modules, classes, scripts et al from the
# "common" directory, which helps keep the code more modular while also
# grouping scripts together by device type and/or purpose

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities

logging.basicConfig(filename='hardwareDataWindows.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def monitor(client, data, topic):

    logging.debug('HW monitoring started')

    while True:

        # get Windows Data
        bigFreq, littleFreq, cpuTemp = data.getLibreData()

        # get GPU utilization
        gpuTemp, gpuUtilization, vramUse, gpuPower, gpuClock = data.gpuQuery()

        # get CPU load
        cpuLoad = data.getCPUData()

        # get RAM use
        ramUse = data.getRAM()

        payload = {
            "gpuTemp": gpuTemp,
            "cpuTemp": cpuTemp,
            "cpuFreqBig": bigFreq,
            "cpuFreqLittle": littleFreq,
            "gpuLoad": gpuUtilization,
            "cpuLoad": cpuLoad,
            "ramUtilization": ramUse,
            "vramUtilization": vramUse,
            "gpuClock": gpuClock,
            "gpuPower": gpuPower
            }

        payload = json.dumps(payload)

        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f'Data {payload} was published to: {topic} with status:\
                  {status}')
        else:
            print(f'Failed to send {payload} to: {topic}')

        del payload, gpuTemp, cpuTemp, bigFreq, littleFreq, gpuUtilization, \
            cpuLoad, ramUse, vramUse,
        gpuClock, gpuPower

        gc.collect()
        time.sleep(1)


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

    # instantiate CPU data class
    winData = WindowsSensors()

    # start monitoring
    try:
        monitor(client, winData, topic)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
