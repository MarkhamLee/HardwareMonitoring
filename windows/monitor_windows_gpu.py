# Markham Lee (C) 2023 - 2024
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# script to retrieve Windows data and publish it to an MQTT topic
# leverages psutil + the LibreHardwareMonitor library
import json
import gc
import os
import sys
import time
from windows_data import WindowsSensors

# this allows us to import commonly used modules, classes, scripts et al
# from the "common" directory, so the code is more modular

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.device_tool import DeviceUtilities  # noqa: E402
from common.nvidia_gpu import NvidiaSensors  # noqa: E402
from common.logging_util import logger  # noqa: E402


def monitor(client: object, cpu_data: object, gpu_data: object, TOPIC: str):

    logger.info('Windows HW monitoring started....')

    INTERVAL = int(os.environ['GAME_INTERVAL'])

    while True:

        # get CPU data clock speed and temperature
        big_freq, little_freq, cpu_temp = cpu_data.get_libre_data()

        # get GPU data
        gpu_temp, gpu_utilization, vram_use, gpu_power, \
            gpu_clock = gpu_data.gpu_query()

        # get FPS data
        gpu_fps = gpu_data.gpu_fps()

        # get CPU load
        cpu_load = cpu_data.get_cpu_data()

        # get RAM use
        ram_use = cpu_data.get_ram()

        payload = {
            "gpuTemp": gpu_temp,
            "cpuTemp": cpu_temp,
            "cpuFreqBig": big_freq,
            "cpuFreqLittle": little_freq,
            "gpuLoad": gpu_utilization,
            "cpuLoad": cpu_load,
            "ramUtilization": ram_use,
            "vramUtilization": vram_use,
            "gpuClock": gpu_clock,
            "gpuPower": gpu_power,
            "fps": gpu_fps
        }

        payload = json.dumps(payload)

        result = client.publish(TOPIC, payload)
        status = result[0]
        if status != 0:
            logger.debug(f'Failed to send {payload} to: {TOPIC}')

        del payload, gpu_temp, cpu_temp, big_freq, little_freq, \
            gpu_utilization, cpu_load, ram_use, vram_use, \
            gpu_clock, gpu_power

        gc.collect()
        time.sleep(INTERVAL)


def main():

    # instantiate utilities class
    device_utilities = DeviceUtilities()

    # operating parameters
    TOPIC = os.environ['GAME_TOPIC']

    # load environmental variables
    MQTT_BROKER = os.environ["MQTT_BROKER"]
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    client_id = device_utilities.get_client_id()

    # get mqtt client
    client, code = device_utilities.mqtt_client(client_id, MQTT_USER,
                                                MQTT_SECRET,
                                                MQTT_BROKER,
                                                MQTT_PORT)

    # instantiate CPU data class
    win_data = WindowsSensors()

    # instantiate the NVIDIA GPU class
    gpu_data = NvidiaSensors()

    # start monitoring
    try:
        monitor(client, win_data, gpu_data, TOPIC)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
