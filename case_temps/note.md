### Quick Notes

* Built this container for automation purposes, it just runs in the background and when the machine runs hot enough it transmits data. Saves me from having to start up the case temperature monitoring script by hand, before I do something resource intensive like gaming or training ML models. 
* main.py replaces the caseTemps.py file, it doesn't need the device tools external script as it's all combined into one. This change was made to reduce the number of files needed to build the Docker image.
* To run the Docker container on Portainer you'll need to pass the "device" parameter to enable the Docker container to access the GPIO pins:
    * When deploying the container go to:
        * Runtime 
        * Add device
        * Put in /dev/gpiomem for both the host and the container 
    * With the docker run command add: --device /dev/gpiomem 
* If you were deploying it via Kubernetes you just need to give the container elevated permissions so it can access the GPIO pins. <-- finding a more secure way to do this is on my list of TODOs