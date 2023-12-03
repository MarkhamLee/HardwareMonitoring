# Markham Lee 2023
# Hardware Monitor: https://github.com/MarkhamLee/HardwareMonitoring
# the script gathers data from three DHT22 temperature sensors and then
# publishes that data to a MQTT topic.

import adafruit_dht
import board
import json
import time
import gc
import os
import logging
import uuid
from paho.mqtt import client as mqtt

# setup logging for static methods
logging.basicConfig(filename='hardwareData.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


def getTemps(client: object, topic: object, interval: int):

    # the use pulseio parameter is suggested parameter for a Raspberry Pi
    # may not need to use it with other types of SBCs
    interior_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    exhaust_device = adafruit_dht.DHT22(board.D5, use_pulseio=False)
    intake_device = adafruit_dht.DHT22(board.D6, use_pulseio=False)

    while True:

        # get temperature and humidity data, not using humidity at the moment,
        # but may use in the future TODO: add exception handling, i.e. log
        # when one of the individual sensors is offline or malfunctioning
        # these sensors are kind of "slow" takes a few seconds to gather data
        # from each one

        try:
            temp_interior = interior_device.temperature
            temp_exhaust = exhaust_device.temperature
            temp_intake = intake_device.temperature

        except RuntimeError as error:
            logging.debug(f'Device runtime error {error}')

            # TODO: mqtt message to note device read error,
            # log said errors in a DB for later analysis
            time.sleep(10)
            continue

        except Exception as error:
            logging.debug(f'Device read error {error}')
            time.sleep(10)
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
            time.sleep(600)
            continue

        payload = {
                "ct": temp_interior,
                "et": temp_exhaust,
                "it": temp_intake,
                "hf": heating_factor
        }

        payload = json.dumps(payload)
        print(payload)

        try:
            result = client.publish(topic, payload)
            status = result[0]

        except Exception as error:
            logging.debug(f'MQTT connection error: {error}\
                          with status: {status}')

        # given that this is a RAM constrained device,
        # let's delete everything and do some garbage collection,
        # watching things on htop the RAM usage was creeping upwards...

        del payload, temp_interior, temp_exhaust, status, result
        gc.collect()

        time.sleep(interval)


def mqttClient(clientID: str, username: str, pwd: str,
               host: str, port: int):

    def connectionStatus(client, userdata, flags, code):

        if code == 0:
            print('connected')

        else:
            print(f'connection error: {code} retrying...')
            logging.DEBUG(f'connection error occured, return code: {code}')

    client = mqtt.Client(clientID)
    client.username_pw_set(username=username, password=pwd)
    client.on_connect = connectionStatus

    code = client.connect(host, port)

    # this is so that the client will attempt to reconnect automatically/
    # no need to add reconnect
    # logic.
    client.loop_start()

    return client, code


def getClientID():

    clientID = str(uuid.uuid4())

    return clientID


def main():

    # load environmental variables
    TOPIC = os.environ['TOPIC']
    INTERVAL = int(os.environ['INTERVAL'])
    MQTT_BROKER = os.environ['MQTT_BROKER']
    MQTT_USER = os.environ['MQTT_USER']
    MQTT_SECRET = os.environ['MQTT_SECRET']
    MQTT_PORT = int(os.environ['MQTT_PORT'])

    # get unique client ID
    clientID = getClientID()

    # get mqtt client
    client, code = mqttClient(clientID, MQTT_USER,
                              MQTT_SECRET, MQTT_BROKER,
                              MQTT_PORT)

    # start data monitoring
    try:
        getTemps(client, TOPIC, INTERVAL)

    finally:
        client.loop_stop()


if __name__ == '__main__':
    main()
