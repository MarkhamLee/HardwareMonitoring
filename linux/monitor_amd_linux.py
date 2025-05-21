#!/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# This is for Linux devices running on AMD CPUs
# CLI instructions file_name + <MQTT topic name as a string>
# + <Integer for sleep interval>
# e.g., python3 monitor_amd_linux.py '/home/amd' 5
import json
import os
import sys
from time import sleep
from linux_cpu_data import LinuxCpuData

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.device_tool import DeviceUtilities  # noqa: E402
from common.logging_util import console_logging  # noqa: E402

logger = console_logging('amd_linux_monitoring')


def monitor(client: object, get_data: object, TOPIC: str, INTERVAL: int):

    while True:

        # get CPU utilization
        cpu_util = get_data.get_cpu_data()

        # get current RAM use
        ram_util = get_data.get_ram_data()

        # get current freq and core count
        cpu_freq, core_count = get_data.get_freq()

        # get CPU, GPU and NVME temperatures
        nvme_temp, cpu_temp, amdgpu_temp = get_data.amd_linux_data()

        payload = {
            "cpu_temp": cpu_temp,
            "amdgpu_temp": amdgpu_temp,
            "nvme_temp": nvme_temp,
            "cpu_freq": cpu_freq,
            "cpu_use": cpu_util,
            "ram_use": ram_util
        }

        payload = json.dumps(payload)
        logger.info(payload)

        result = client.publish(TOPIC, payload)
        status = result[0]

        if status != 0:
            print(f'Failed to send {payload} to: {TOPIC}')
            logger.debug(f'MQTT publishing failure, return code: {status}')

        sleep(INTERVAL)


def main():

    # instantiate utilities class
    device_utilities = DeviceUtilities()

    # parse command line arguments
    args = sys.argv[1:]

    TOPIC = args[0]
    INTERVAL = args[1]

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    client_id = device_utilities.get_client_id()

    # get mqtt client
    client, code = device_utilities.mqtt_client(client_id, MQTT_USER,
                                                MQTT_SECRET, MQTT_BROKER,
                                                MQTT_PORT)

    # instantiate CPU & GPU data classes
    get_data = LinuxCpuData()

    logger.info('Starting HW monitoring')

    # start data monitoring
    try:
        monitor(client, get_data, TOPIC, INTERVAL)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
