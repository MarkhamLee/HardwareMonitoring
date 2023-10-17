# Markham Lee 2023 
# Hardware Monitor: https://github.com/MarkhamLee/hardware-monitor
# the script gathers data from two DHT22 temperature sensors and then publishes that data 
# to a MQTT topic 
# Also, can strip out all the MQTT stuff and just use the DHT22 code for building a weather station 
# or IoT temperature sensor with a Raspberry Pi or other single board computer 


import Adafruit_DHT
import json
import time
import gc
import os 
import sys
import logging
from paho.mqtt import client as mqtt

# this allows us to import modules, classes, scripts et al from the "common" directory 
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.deviceTools import DeviceUtilities

# setup logging for static methods 
logging.basicConfig(filename='hardwareData.log', level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def getTemps(client, topic, interval=30):
        
        while True:
               
                # get temperature and humidity data, not using humidity at the moment, but may use in the future
                # TODO: add exception handling, i.e. log when one of the individual sensors is offline or malfunctioning 
                # these sensors are kind of "slow" takes a few secodns to gather data from each one 
                hum_interior, temp_interior = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
                hum_exhaust, temp_exhaust = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 5)
                hum_intake, temp_intake = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 6)

                temp_interior = round(temp_interior, 2)
                temp_exhaust = round(temp_exhaust, 2)
                temp_intake = round(temp_intake, 2)

                # heating factor refers to the difference in the temperature of the intake air coming into the front of case vs the exhaust air coming out of the top of the case 
                heating_factor = round((temp_exhaust - temp_intake), 3) 


                payload = {
                
                "ct": temp_interior,
                "et": temp_exhaust,
                "it": temp_intake,
                "hf": heating_factor
                 
                 }

                payload = json.dumps(payload)

                result = client.publish(topic, payload)
                status = result[0]
        
                if status == 0:
                        print(f'Data {payload} was published to: {topic}')
                else:
                        print(f'Failed to send {payload} to: {topic}')
                        logging.debug(f'data failed to publish to MQTT topic, status code: {status}')

                # given that this is a RAM constrained device, let's delete everything and 
                # do some garbage collection, watching things on htop the RAM usage was creeping upwards... 
                del payload, hum_exhaust, hum_interior, hum_intake, temp_interior, temp_exhaust, status, result 
                gc.collect()

                time.sleep(interval)


def main():
    
    # instantiate utilities class 
    deviceUtilities = DeviceUtilities()

    # parse command line arguments 
    args = sys.argv[1:]

    configFile = args[0]
    secrets = args[1]
    interval = int(args[2])

    broker, port, topic, user, pwd = deviceUtilities.loadConfigs(configFile, secrets)

    # get unique client ID 
    clientID = deviceUtilities.getClientID()

    # get mqtt client    
    client, code = deviceUtilities.mqttClient(clientID, user, pwd, broker, port)

    # start data monitoring 
    try:
        getTemps(client, topic, interval)

    finally:
        client.loop_stop() 


if __name__ == '__main__':
      main() 
