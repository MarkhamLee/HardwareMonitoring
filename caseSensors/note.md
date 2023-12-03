### Quick Notes

* Built this container for automation purposes, it just runs in the background and when the machine runs hot enough it transmits data. Saves me from having to start up the case temperature monitoring script by hand, before I do something resource intensive like gaming or training ML models. 
* main.py replaces the caseTemps.py file, it doesn't need the device tools external script as it's all combined into one. This change was made to reduce the number of files needed to build the Docker image.
* To run the Docker container you'll need to pass the "device" parameter to enable the Docker container to access the GPIO pins:
    * Portainer: (when building the container) go to:
        * Runtime 
        * Add device
        * Put in /dev/gpiomem for both the host and the container 
    * With the docker run command add: --device /dev/gpiomem 