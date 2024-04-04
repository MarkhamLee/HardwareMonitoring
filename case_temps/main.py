# Markham Lee 2023
# Hardware Monitor: https://github.com/MarkhamLee/HardwareMonitoring
# the script gathers data from three DHT22 temperature sensors and then
# publishes that data to a MQTT topic.
import adafruit_dht
import board
import json
import gc
import os
import sys
from time import sleep

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.logging_util import logger  # noqa: E402
from common.device_tool import DeviceUtilities  # noqa: E402

device_utilities = DeviceUtilities()


def get_temps(client: object, TOPIC: object,
              INTERVAL: int, SLEEP_DURATION: int):

    # the use pulseio parameter is suggested parameter for a Raspberry Pi
    # may not need to use it with other types of SBCs
    interior_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    exhaust_device = adafruit_dht.DHT22(board.D5, use_pulseio=False)
    intake_device = adafruit_dht.DHT22(board.D6, use_pulseio=False)

    logger.info('Starting PC Case temperature monitoring...')

    while True:

        # get temperature and humidity data, not using humidity at the moment,
        # but may use in the future TODO: refactor to use different/better
        # sensors as the DHT22 returns read errors about 1/3 of the time.

        try:
            temp_interior = interior_device.temperature
            temp_exhaust = exhaust_device.temperature
            temp_intake = intake_device.temperature

        except RuntimeError as error:
            logger.debug(f'Device runtime error {error}')

            # TODO: mqtt message to note device read error,
            # log said errors in a DB for later analysis
            sleep(10)
            continue

        except Exception as error:
            logger.debug(f'Device read error {error}')
            sleep(10)
            continue

        temp_exhaust = round(temp_exhaust, 2)
        temp_intake = round(temp_intake, 2)

        # heating factor refers to the difference in the temperature of the
        # intake air coming into the front of case vs the exhaust air
        # coming out of the top of the case

        heating_factor = round((temp_exhaust - temp_intake), 3)
        temp_interior = round(temp_interior, 2)

        # This quick check is so that only sends data under high
        # activity. I.e. under normal use this number is around 4-5,
        # it only gets above that if I'm playing games or training
        # ML models

        if heating_factor < 3:
            sleep(SLEEP_DURATION)
            continue

        payload = {
            "ct": temp_interior,
            "et": temp_exhaust,
            "it": temp_intake,
            "hf": heating_factor
        }

        payload = json.dumps(payload)

        try:
            result = client.publish(TOPIC, payload)
            status = result[0]

        except Exception as error:
            logger.debug(f'MQTT connection error: {error}\
                          with status: {status}')

        # given that this is a RAM constrained device,
        # let's delete everything and do some garbage collection,
        # watching things on htop the RAM usage was creeping upwards...

        del payload, temp_interior, temp_exhaust, status, result
        gc.collect()

        sleep(INTERVAL)


def main():

    # load environmental variables
    SLEEP_DURATION = int(os.environ['SLEEP_DURATION'])
    TOPIC = os.environ['TOPIC']
    INTERVAL = int(os.environ['INTERVAL'])
    MQTT_BROKER = os.environ['MQTT_BROKER']
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    client_id = device_utilities.get_client_id()

    # get mqtt client
    client, code = device_utilities.mqtt_client(client_id, MQTT_USER,
                                                MQTT_SECRET, MQTT_BROKER,
                                                MQTT_PORT)

    # start data monitoring
    try:
        get_temps(client, TOPIC, INTERVAL, SLEEP_DURATION)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
