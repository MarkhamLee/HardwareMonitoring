## PC Case Temps via an ESP32

I wanted to spin up another case temp monitor for my ML workstation and decided to use an ESP32 this time around instead of a Raspberry Pico, the reasons are about 70% technical as I have a dozen or so ESP32s that are already provisioned with Wi-Fi and MQTT creds stored on the device and 30% aesthetic as I think the ESP32 will look "cooler" in my workstation case vs the Pico. 

Feature wise, ESP32 vs Pico is close, except for:
    * ESP32 lacks the exception handling of the Pico
    * ESP32 isn't (yet) reporting its CPU temp

One feature the ESP32 variant has that the Pico one doesn't, is that it flashes the blue LED on and off when reading and transmitting data, which is helpful as far as a quick diagnostic as a solid blue LED = something isn't working properly.

