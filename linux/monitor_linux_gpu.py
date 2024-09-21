# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# For Linux devices with an NVIDIA GPU
import json
import gc
import logging
import os
import sys
from time import sleep
from linux_cpu_data import LinuxCpuData

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.device_tool import DeviceUtilities  # noqa: E402
from common.nvidia_gpu import NvidiaSensors  # noqa: E402
from common.logging_util import logger  # noqa: E402


def monitor(client: object, get_data: object,
            get_gpu_data: object, TOPIC: str, INTERVAL: int):

    logger.info('Starting monitoring...')

    while True:

        # get CPU utilization
        cpu_util = get_data.get_cpu_data()

        # get current RAM use
        ram_use = get_data.get_ram_data()

        # get current freq and core count
        cpu_freq, core_count = get_data.get_freq()

        # get CPU temperature
        cpu_temp = get_data.core_temp()

        # get GPU Data
        temp, gpu_load, gpu_vram, gpu_power, \
            gpu_clock = get_gpu_data.gpu_query()

        # build payload
        payload = {
            "cpuTemp": cpu_temp,
            "cpuFreq": cpu_freq,
            "cpuUse": cpu_util,
            "ramUse": ram_use,
            "gpuTemp": temp,
            "gpuLoad": gpu_load,
            "gpuVram": gpu_vram,
            "gpuPower": gpu_power,
            "gpuClock": gpu_clock
        }

        payload = json.dumps(payload)

        result = client.publish(TOPIC, payload)
        status = result[0]
        if status != 0:

            print(f'Failed to send {payload} to: {TOPIC}')
            logging.debug(f'MQTT publishing failure, return code: {status}')

        del payload, cpu_util, ram_use, cpu_freq, cpu_temp, status, \
            result, gpu_load, gpu_vram, gpu_power, gpu_clock
        gc.collect()
        sleep(INTERVAL)


def main():

    # instantiate utilities class
    device_utilities = DeviceUtilities()

    # load environmental variables
    TOPIC = int(os.environ['TOPIC'])
    INTERVAL = os.environ['INTERVAL']
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
    get_gpu_data = NvidiaSensors()
    get_data = LinuxCpuData()

    # start monitoring
    try:
        monitor(client, get_data, get_gpu_data, TOPIC, INTERVAL)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
