/*
* Pulls data froma three different DHT22 temperature and humidity sensors,
to track intake, interior and exhaust temperatures in a PC case, and then
transmit the data via MQTT. 
*/

#include <iostream>
#include <stdlib.h>
#include <Arduino.h>
#include <WiFiManager.h> 
#include <PicoMQTT.h>
#include <ArduinoJson.h>
#include <Preferences.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHT_SENSOR_PIN_18 18 // interior temperature
#define DHT_SENSOR_PIN_19 19 // intake temperatures
#define DHT_SENSOR_PIN_21 21 // exhaust temperature
#define DHT_SENSOR_TYPE DHT22

DHT dht_sensor(DHT_SENSOR_PIN_18, DHT_SENSOR_TYPE);
DHT dht_sensorb(DHT_SENSOR_PIN_19, DHT_SENSOR_TYPE);
DHT dht_sensorc(DHT_SENSOR_PIN_21, DHT_SENSOR_TYPE);


#define LED 2

PicoMQTT::Client mqtt("");

String topic = "/hardware/ml_workstation_case_temps";

void setup() {
  


    WiFi.mode(WIFI_STA); // explicitly set mode, esp defaults to STA+AP
    // it is a good practice to make sure your code sets wifi mode how you want it.
 
    // put your setup code here, to run once:
    Serial.begin(115200);
    
    //WiFiManager, Local intialization. Once its business is done, there is no need to keep it around
    WiFiManager wm;

    // Supress Debug information
    // wm.setDebugOutput(false);
 
    // reset settings - wipe stored credentials for testing
    // these are stored by the esp library
    // wm.resetSettings();

    // bool res;
    // res = wm.autoConnect("esp_setup1", "password");

    // Automatically connect using saved credentials,
    // if connection fails, it starts an access point with the specified name ( "AutoConnectAP"),
    // if empty will auto generate SSID, if password is blank it will be anonymous AP (wm.autoConnect())
    // then goes into a blocking loop awaiting configuration and will return success result
    
    digitalWrite(LED,HIGH);
    if (!wm.autoConnect("esp32_ml_workstation_case_temp", "password")) {
        // Did not connect, print error message
        Serial.println("failed to connect and hit timeout");
    
        // Reset and try again
        ESP.restart();
        delay(1000);
    }
    
    // Connected!
    Serial.println("WiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(LED,LOW);

    /*
    Preferences prefs;

    prefs.begin("credentials", false);

    // Comment out after you've saved the creds. Note: you can apply
    // the below to any vars you want to store on the device. Just be
    // mindful of the limited space.
    
    const char* mqtt_user = MQTT_USER;
    const char* mqtt_secret = MQTT_SECRET;
    const char* mqtt_host = MQTT_HOST;

    prefs.putString("mqtt_user", mqtt_user);
    prefs.putString("mqtt_secret", mqtt_secret);
    prefs.putString("mqtt_host", mqtt_host);

    Serial.println("MQTT credentials saved");

    prefs.end();

    */
     

    Preferences preferences;

    preferences.begin("credentials", false);

    String host = preferences.getString("mqtt_host", "");
    String user = preferences.getString("mqtt_user", "");
    String secret = preferences.getString("mqtt_secret", "");
    Serial.println("MQTT Credentials Loaded");


    // MQTT setup
    mqtt.host=host;
    mqtt.port=1883;
    mqtt.username = user;
    mqtt.password= secret;
    mqtt.client_id = "esp32_ml_workstation_temp_monitor";
    mqtt.begin();
    
    // setup pin to flash on activity
    pinMode(LED, OUTPUT);
    Serial.println("MQTT running");
    

    // set up for DHT22 sensor 
    Serial.begin(9600);
    dht_sensor.begin();  // initialize sensor
    dht_sensorb.begin(); //initialize sensor
    dht_sensorc.begin(); //initialize sensor


}


void loop() {

  mqtt.loop();

  // sensor 0
  // read humidity
  digitalWrite(LED,HIGH); 
  float humi  = dht_sensor.readHumidity();
  // read temperature in Celsius
  float tempC = dht_sensor.readTemperature();
 

  // sensor 1
  // read humidity
 
  float humi_1  = dht_sensorb.readHumidity();
  // read temperature in Celsius
  float tempC_1 = dht_sensorb.readTemperature();


  // sensor 2
  // read humidity
  
  float humi_2  = dht_sensorc.readHumidity();
  // read temperature in Celsius
  float tempC_2 = dht_sensorc.readTemperature();
 

  // check whether the reading is successful or not
  if ( isnan(tempC) || isnan(humi)) {
    Serial.println("Failed to read from DHT sensor!");
    
    // TODO: add logic for sending alerts for device read failures
    // initial approach will be to send a MQTT message to count how often this occurs
    // before we spam ourselves with alert messages.

  } else {

    double hf = tempC_2 - tempC;

    // build JSON message for MQTT 
    JsonDocument payload; // define json document

    //Add data to the JSON document 
    payload["interior_temperature"] = tempC;
    payload["interior_humidity"] = humi;

   
    payload["intake_temperature"] = tempC_1;
    payload["intake_humidity"] = humi_1;

   
    payload["exhaust_temperature"] = tempC_2;
    payload["exhaust_humidity"] = humi_2;

    payload["heating_factor"] = hf;

    // send MQTT message
    Serial.println("Sending MQTT message: ");
    auto publish = mqtt.begin_publish(topic, measureJson(payload));
    serializeJson(payload, publish);
    publish.send();
    digitalWrite(LED,LOW);

    Serial.begin(115200);
    // output payload in json format for monitoring and testing, can be commented out
    serializeJsonPretty(payload, Serial);
    Serial.println();
  
  }

  // sleep interval of five seconds 
  delay(5000);
  

 
}