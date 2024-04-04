#!/usr/bin/env python
# this would be for linux devices where I'm not using an NVIDIA GPU/a GPU at all, e.g. 
# single board computers running headless, or devices like an Intel NUC, so I would only
# monitor the CPU 

import json
import time 
from paho.mqtt import client as mqtt 
import gc 
import subprocess as sp
import os
import logging
import sys


# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)


from common.device_tool import DeviceUtilities

logging.basicConfig(filename='hardwareData.log', level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def monitor(client, getData. topic):

    while True: 

        time.sleep(1)

        #insert calls to data retrieval methods here 



        gc.collect() 


def main(): 

    # instantiate utilities class 
    deviceUtilities = DeviceUtilities()

    # parse command line arguments 
    args = sys.argv[1:]

    configFile = args[0]
    secrets = args[1]

    # load config file(s)
    broker, port, topic, user, pwd = deviceUtilities.loadConfigs(configFile, secrets)


    # get unique client ID 
    clientID = deviceUtilities.getClientID()

    # get mqtt client    
    client, code = deviceUtilities.mqttClient(clientID, user, pwd, broker, port)

    # instantiate data classes - pass the object for the data class into the call to the monitor function 
    getData = someMethod() 

    # start monitoring 
    try:
        monitor(client, getData, topic)

    finally:
        client.loop_stop()

    
if __name__ == '__main__':
      main() 