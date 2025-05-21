## Gaming PC Sensor Panel & General Hardware Monitoring

What started out as me toying around with some ideas for a solution to monitor case temps + hardware for a single board computer cluster I'm building, turned into, *"gamer/engineer finds way to prototype a monitoring solution for his cluster project, while also building an unnecessary but fun monitoring solution for his gaming PC"*. Because, as we all know, you definitely need to know the difference in temperature between the air going in and coming out of your gaming PC while playing heavily modded (e.g., ENB, updated animations, AI and other resource intensive mods) Fallout 4 or Skyrim... in case you're wondering the exhaust air is (on average) 11.4 degrees Celsius hotter than the intake air. Jokes aside, my eventual plan is that this will be the basis of a "smart" cooling system for the cluster, where the fans for the individual SBCs and the case will be controlled independently of the individual devices themselves, based on the temperatures of the room, air intake, air exhaust and the on-board CPU, NVME, et al, sensors. I am not sure that this would provide better cooling, even if my updated fan controller is "smart" but finding out should be a fun endeavor.  

TL/DR: *"you like computers bro? Okay, but did you put a small computer inside your big computer to send data about the big computer’s case to another computer?"*  

Also: I'm fully aware there are numerous off the shelf solutions for PC monitoring, but having more granular control helps in situations where variances in MOBOs, coolers and the like result in the wrong data being picked up (*E.g., fans and water coolers via AIDA64 on my setup*), plus it's easier to incorporate data from external sources. Currently, this project could be viewed as an *"aggregating data for a PC Sensor Panel solution, baseline scripts for being monitoring Linux hardware for use in other projects"* E.g., [my data platform project](https://github.com/MarkhamLee/finance-productivity-iot-informational-weather-dashboard/tree/main/hardware_telemetry) and my [Kubernetes cluster project](https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-platform) 


**Heavily, heavily modded Skyrim, 4k textures, vastly improved graphics and character models, parallax mods, updated animations, updated combat, engine upgrades to enable FPS above 60 FPS without breaking the engine/causing weird visual artifacts, etc., running in 4k @ 180+ FPS --- *it's basically Eldenrim at this point...*** 
![Dashboard Screenshot](/images/updated_screenshot.png)  

### Updates

* **05/20/2025**
    * Updated DLLs to ensure compatibility with the latest Hardware
    * Tested/verified that Windows data monitoring works with Intel Ultra processors
    * Updated Python dependencies
    * Added more detailed instructions for setting up LibreHardwareMonitor, troubleshooting/gotchas that can occur with the DLLs. 

* **04/03/24**
    * Added GitHub Actions config for building the Docker image for collecting PC case data with a Raspberry Pi 4B 
    * Extensive refactoring and code clean-up, normalizing variable names, streamling code where possible, etc.
    * Rebuilt Dockerfile: two stage image build is smaller and more secure
    * Removed the code for the single board computers, as it's being maintained as part of my [Kubernetes Project](https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-platform/tree/main/hardware_monitoring) and my [Data platform project](https://github.com/MarkhamLee/finance-productivity-iot-informational-weather-dashboard/tree/main/hardware_telemetry). That code has also been rebuilt to be deployed as Docker containers that continuously provide telemetry data, rather than scripts you run from the command line. 
    * Added script/firmware for PC case data collection with a Raspberry Pi Pico (Jan '24)


#### How to run it
* The general pattern to run the device specific scripts is to store your credentials for MQTT, the topic and refresh interval as environmental variables, and then use the command line pattern of python + file name.  

*  For case temperatures you have two options: 

	* You can build and deploy the container in the case_temps folder to a Raspberry Pi or a single board computer with similar pin outs, libraries, etc., to retrieve data from DHT22 temperature sensors 
	* You could flash a Raspberry Pi Pico with the code in the case_temps_rpi_pico folder 

Once you have chosen one of the above, you just need to position the sensors, connect the temperature sensors, and then connect power to your device. The Pico will constantly transmit data and the Raspberry Pi will only transmit data when the delta between intake and exhaust air exceeds a pre-defined threshold. 

* Note: while GPU and CPUs can have very quick frequency, temperature and load changes, case air temperature changes are not as rapid, so it doesn't need to refresh every second like the hardware sensors.  
* Detailed GPU monitoring (VRAM, Clock Freq, Power Draw) only works for NVIDIA GPUs; however, the solution can monitor temperatures for Rockchip 3588 GPUs and NPUs. 
* Has been tested with Intel X86 CPUs, Raspberry Pi 4bs and Rockchip 3566 & 3588 CPUs/System on a Chip (SOCs), AMD Ryzen 5 5560U & Armlogic AML-S905X-CC. For other platforms you can use the hardware_scan.py in the Linux folder to generate a json of the available data/sensors on your device. 

### Tech Stack 
My initial setup was running the items below on a Raspberry Pi 4B, but I subsequently a built a more complex data ingestion platform that runs on a K3S – Kubernetes cluster and that is where the tech stack currently lives.  That said, I want to stress that *you do not need a complex cluster to run this solution*, a single Raspberry Pi + Portainer is all you need to run the apps below and it would have no problem logging data for several machines at once.  

* Mosquitto for receiving MQTT messages 
* InfluxDB for storing the data 
* Grafana for visualization, my original plan was to use Streamlit, but after seeing how easy it was to configure Grafana, I decided to switch course  
* I also used node-red for quickly wiring and configuring things like Mosquitto to Influx to Grafana 

#### What we have so far: 
* Scripts for Linux machines with NVIDIA GPUs, scripts for Linux Machines without dedicated GPUs & Linux machines running AMD CPUs w/ integrated AMD GPUs.  
* All GPU data acquired directly from the GPU via NVIDIA SMI queries  
* Scripts for Windows machines with NVIDIA GPUs, plus separate scripts for Linux machines without NVIDIA GPUs/Dedicated GPUs   
* Scripts for Rockchip 3588 Running Ubuntu 
* Scripts for Rockchip 3566 devices  
* Scripts for AMD Ryzen 5 mobile CPUs (tested on AMD 5560U) 
* Scripts for Raspberry Pi 4Bs running the official headless Ubuntu distro for Raspberry Pi 
* Scripts for Libre Computer Le Potato running the AML-S905X-CC chip 
* Scripts to gather data from three DHT22 temperature sensors connected to a Raspberry Pi or Raspberry Pi Pico to gather intake air, internal case, and exhaust temperatures  


#### Things I want to add/do in the future:
* Dynamically scan and collect data on the hardware and then adjust data collection accordingly  
* Add FPS data to the Windows script(s)  
* CPU load per core  
* Fan speeds: desktop cases, desktop GPUs, individual fans on SBCs, fans in cluster cases  
* Find ways to get CPU clock speed and CPU and GPU temperatures on Windows and/or just possibly source data direct from AIDA64, so I don't need to use the Librehardwaremonitor library 
* Ability to add an "activity flag" to the data, I.e., game vs machine learning on my Windows machine.  
* Use something like a Raspberry Pi Pico or to control case fans (for SBC cluster) depending on temperatures 


#### Acknowledgements, shout-outs and the like 
* [The LibreHardwareMonitor Team - Repo](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor), which I used to monitor my W11 machine in instances psutil or GPUutil wasn't able to access certaiin sensors on Windows
* I used [Matthieu Houdebine's Turing Smart Screen Repo](https://github.com/mathoudebine/turing-smart-screen-python) as a reference around how to use the LibreHardwareMonitor DLLs with Python 

#### Technical Details 
* Used a variety of machines given that a lot of the code is tailored towards certain devices, namely: 12th Gen i7 w/ NVIDIA 3090TI running W11, 12th Gen Intel NUC, Beelink SER5 Pro, Orange Pi 3B, 11th Gen i5 w/ 3060TI all running Ubuntu 22.04, Orange Pi 5 Plus running [Joshua Riek's Ubuntu distribution for Rockchip 3588 devices](https://github.com/Joshua-Riek/ubuntu-rockchip) 
