import network
import dht
import keyData
import ujson
import gc
from umqtt.simple import MQTTClient
from machine import Pin, ADC
from time import sleep


gc.enable()


# method for connecting to Wi-Fi
def network_connect():

    SSID = keyData.SSID
    SECRET = keyData.SECRET_W

    connection = network.WLAN(network.STA_IF)
    connection.active(True)

    try:
        connection.connect(SSID, SECRET)
        print(f'connected to Wi-Fi: {SSID}')

    except Exception as e:
        print(f'connection to Wi-Fi failed: {e}')

    while connection.isconnected() == False:
        pass


def mqtt_connect():

    CLIENT_ID = keyData.clientID

    client = MQTTClient(
        client_id=CLIENT_ID,
        server=keyData.broker,
        user=keyData.user,
        password=keyData.secret,
        keepalive=3600,
        ssl_params={'server_hostname': keyData.broker})

    # client = MQTTClient(client_id, mqtt_server, keepalive=3600)

    client.connect()
    print('Connected to MQTT Broker')

    return client


def reconnect():
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    sleep(5)
    machine.reset()


# connect to the sensor - create sensor object
def sensor_connect(pin0: int, pin1: int, pin2: int) -> object:

    # connect to DHT22 temperature sensors
    interior = dht.DHT22(Pin(pin0))
    intake = dht.DHT22(Pin(pin1))
    exhaust = dht.DHT22(Pin(pin2))

    # connect to built in temperature sensor
    adcpin = 4
    sensor = ADC(adcpin)

    return interior, intake, exhaust, sensor


# get sensor data
def get_case_temps(interior: object, intake: object, exhaust: object,
                   sensor: object, client, topic):

    while True:

        try:

            interior.measure()
            interior_temp = interior.temperature()
            interior_humidity = interior.humidity()

            intake.measure()
            intake_temp = intake.temperature()
            intake_humidity = intake.humidity()

            exhaust.measure()
            exhaust_temp = exhaust.temperature()
            exhaust_humidity = exhaust.humidity()

            # create json payload
            hf = exhaust_temp - intake_temp
            hf = round(hf, 3)

            # get Raspberry Pico temp from internal temp sensor
            device_temp = get_device_temps(sensor)

            payload = {
                "ct": interior_temp,
                "case_humidity": interior_humidity,
                "et": exhaust_temp,
                "exhaust_humidity": exhaust_humidity,
                "it": intake_temp,
                "intake_humidity": intake_humidity,
                "hf": hf,
                "pico_temp": device_temp
                }

            payload = ujson.dumps(payload)

            try:
                publish_mqtt(payload, topic, client)
                print('payload published successfully')

            except Exception as e:
                print(f'Failed to publish to MQTT topic {e}')
                machine.reset()

        except Exception as e:
            print(f'failed to read data from sensor')
            machine.reset()

        del payload, hf, exhaust_temp, intake_temp, interior_temp, \
            interior_humidity, exhaust_humidity, intake_humidity, \
            device_temp

        gc.collect()

        sleep(15)


# get Raspberry Pico Device Temps 
def get_device_temps(sensor: object):

    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 2)


# sent MQTT message
def publish_mqtt(payload: dict, topic: str, client: object):

    client.publish(topic, payload)


def main():

    TOPIC = keyData.topic

    network_connect()
    client = mqtt_connect()
    interior, intake, exhaust, sensor = sensor_connect(0, 1, 2) 
    get_case_temps(interior, intake, exhaust, sensor, client, TOPIC)


if __name__ == '__main__':
    main()
