# !/usr/bin/env python
# Markham Lee (C) 2023 - 2024
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# General utilities for sendign data via MQTT and
# scanning a device to see the available sensors
import psutil
import uuid
from paho.mqtt import client as mqtt
from common.logging_util import logger


class DeviceUtilities():

    # just a placeholder for now
    def __init__(self):

        pass

    @staticmethod
    def get_client_id():

        clientID = str(uuid.uuid4())

        return clientID

    @staticmethod
    def temp_sensor_scan():

        # get the dictionary of all sensor data
        tempDict = psutil.sensors_temperatures()

        # filter out the keys
        sensorList = list(tempDict.keys())

        return sensorList

    @staticmethod
    def mqtt_client(clientID: str, username: str, pwd: str,
                    host: str, port: int):

        def connection_status(client, userdata, flags, code):

            if code == 0:
                print('connected')

            else:
                print(f'connection error: {code} retrying...')
                logger.DEBUG(f'connection error occured, return code: {code}')

        client = mqtt.Client(clientID)
        client.username_pw_set(username=username, password=pwd)
        client.on_connect = connection_status

        code = client.connect(host, port)

        # this is so that the client will attempt to reconnect automatically/
        # no need to add reconnect
        # logic.
        client.loop_start()

        return client, code
