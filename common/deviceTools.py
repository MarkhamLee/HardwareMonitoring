# !/usr/bin/env python
# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/HardwareMonitoring
# simple script to generate unique IDs for each device, uses UUID4
# as that ensures we get a truly unique ID and not one derived from
# the MAC address, with the associated security risks such an
# approach can bring.
# Putting this into its own script (for now) as so the various
# clients can use it + I'll probably put other utilities into this
# script, create an onboarding process, etc.

import uuid
from paho.mqtt import client as mqtt
import logging
import json
import psutil


# setup logging for static methods
logging.basicConfig(filename='hardwareData.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s\
                        : %(message)s')


class DeviceUtilities():

    # just a placeholder for now
    def __init__(self):

        pass

    # method for parsing the config file with connection data +
    # the secrets file
    @staticmethod
    def loadConfigs(configFile, secretsFile):

        with open(configFile, "r") as file:
            data = json.load(file)

        broker = data["broker"]
        port = data["port"]
        topic = data["topic"]

        with open(secretsFile, "r") as secrets:
            data = json.load(secrets)

        user = data["user"]
        password = data["password"]

        return broker, port, topic, user, password

    @staticmethod
    def getClientID():

        clientID = str(uuid.uuid4())

        return clientID

    @staticmethod
    def tempSensorScan():

        # get the dictionary of all sensor data
        tempDict = psutil.sensors_temperatures()

        # filter out the keys
        sensorList = list(tempDict.keys())

        return sensorList

    @staticmethod
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
