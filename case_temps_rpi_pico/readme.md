## PC Case Temps with a Raspberry Pi Pico 

Given the low resource utilization for running three temp sensors on a Raspberry Pi 4B, I decided it waste to use one for that purpose. SO.. I moved the sensors to run off of a Raspberry Pi Pico instead, as the hardware is a better fit for this purpose. The implementation is pretty basic: a simple micropython script starts up whenver the device turns on, captures sensor data and then sends it off via MQTT. 

A couple of notes:

* The code is in micropython so a few things may appear off if you look at the script on an x86 device
* MQTT doesn't always reconnect, and the Wi-Fi authentication method isn't secure enough for my tastes. I.e., finding ways to clean up this code, a more elegant reconnection to the MQTT broker and more secure network connections are all on my list of to dos. 
* Picos are rather resource constrained so garbage collection is critical, without it the device crashes after 5-10 minutes 
* Due to it being a micro-controller the Pico can only do one thing at time, so it doesn't handle python exceptions very well. However, just setting the device to reset if it has a device read or MQTT publish error seemed to resolve those issues. 
* Due to limitations around wire length, I have the Pico positioned near my video card, so I added data from the Pico's onboard temperature sensor so I can see if playing video games or running other heavy GPU workloads will cause the Pico to heat up more than it should. The temps rarely went higher than 24 degrees with my gaming PC turned off and usually hovered around 28 with it turned on.  
