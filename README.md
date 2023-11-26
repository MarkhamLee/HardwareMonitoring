## Hardware Monitoring

What started out as me toying around with some ideas for a solution to monitor case temps + hardware for a single board computer cluster I'm building, turned into, *"gamer/engineer finds way to prototype a monitoring solution for his cluster project, while also building an unnecessary but fun monitoring solution for his gaming PC"*. Because, as we all know, you definitely need to know the difference in temperature between the air going in and coming out of your gaming PC while playing heavily modded (e.g., ENB, updated animations, AI and other resource intensive mods) Fallout 4 or Skyrim... in case you're wondering the exhaust air is (on average) 11.4 degrees celsius hotter than the intake air. Jokes aside, my eventual plan is that this will be the basis of a "smart" cooling system for the cluster, where the fans for the individual SBCs and the case will be controlled independently of the individual devices themselves, based on the temperatures of the room, air intake, air exhaust and the on board CPU, NVME, et al, sensors. I'm not sure that would provide better cooling, even if my updated fan controller is fairly "smart" but finding out should be a fun endeavor. 

TL/DR: *"you like computers bro? Okay, but did you put a small computer inside your big computer to send data about the big computer and the case it's in to another computer?"* 

Also: I'm fully aware there are numerous off the shelf solutions, but having more granular control helps in situations where variances in MOBOs, coolers and the like result in the wrong data being picked up (*E.g., fans and water coolers via AIDA64 on my setup*), plus it's easier to incorporate data from external sources. At this juncture this project could be viewed as an *"aggregating data for a PC Sensor Panel solution, baseline scripts for being monitoring linux hardware for use in other projects"*  E.g., [my data platform project](https://github.com/MarkhamLee/productivity-music-stocks-weather-IoT-dashboard/tree/main/telemetry)


**Heavily, heavily modded Skyrim, 4k textures, vastly improved graphics and character models, parallax mods, updated animations, updated combat, engine upgrades to enable FPS above 60 FPS without breaking the engine/causing weird visual artifacts, etc., running in 4k @ 180+ FPS --- *it's basically Eldenrim at this point...*** 
![Dashboard Screenshot](/images/skyrim3.png)  

#### How to run it
* The windows script CLI pattern is file-name [path to general config json] [path to secrets json], you can use this pattern + the main method as a reference for using json configs with the Linux files. I didn't convert the one Windows script just there is an example of using this with json configs 
* The scripts for Linux, Linux w/ NVIDIA GPU and the single board computers Raspberry Pi & Orange Pi all use the same pattern cli wise: 
    * scriptname.py 'mqtt topic name'
* For the case temps script it's exactly as above, but you have to pass the topic name and a refresh interval 
    * Note: while GPU and CPUs can have very quick frequency, temperature and load changes, case air temperature changes aren't as rapid so it doesn't need to refresh every second like the hardware sensors. 
* At the moment detailed GPU monitoring (VRAM, Clock Freq, Power Draw) only works for NVIDIA GPUs, however, the solution can monitor temperatures for Rockchip 3588 GPUs and NPUs.
* Has been tested with Intel X86 CPUs, Raspberry Pi 4bs and Rockchip 3566 & 3588 CPUs/System on a Chip (SOCs), AMD Ryzen 5 5560U & Amlogic AML-S905X-CC. For other platforms you can use the hardware_scan.py in the Linux folder to get the data on the available CPU & temperature sensors on those devices. An update to hardware scan to gather details on all available sensors is pending. 


#### What we have so far: 
* Scripts for Linux machines with NVIDIA GPUs, scripts for Linux Machines without dedicated GPUs & Linux machines running AMD CPUs w/ integrated AMD GPUs. 
* All GPU data acquired directly from the GPU via NVIDIA SMI queries 
* Scripts for Windows machines with NVIDIA GPUs, plus separate scripts for Linux machines without NVIDIA GPUs/Dedicated GPUs  
* Scripts for Rockchip 3588 Running Ubuntu
* Scripts for Rockchip 3566 devices 
* Scripts for AMD Ryzen 5 mobile CPUs (tested on AMD 5560U)
* Scripts for Raspberry Pi 4Bs running the official headless Ubuntu distro for Raspberry Pi
* Scripts for Libre Computer Le Potato running the AML-S905X-CC chip
* Three DHT22 temperature sensors connected to a Raspberry Pi gather intake air, internal case and exhaust  temperatures 
* Mosquitto for receiving MQTT messages
* InfluxDB for storing the data
* Grafana for visualization, my original plan was to use Streamlit, but after seeing how easy it was to configure Grafana, I decided to switch course 
* I also used node-red for quickly wiring and configuring things like Mosquitto to Influx to Grafana 
* Grafana, InfluxDB, Mosquitto & Node-Red are all running in containers on a Raspberry Pi (separate from the one gathering temp data). I was initially skeptical about Node-Red, but after using it for about two months I'm quite happy with it for small scale tasks or receiving data from IoT sensors. 


#### Things I want to add/do in the future:
* Scan and collect data on the hardware and then adjust data collection accordingly 
* Test the cpu only Linux script on the following devices and make any necessary tweaks for ARM devices: 
    * Raspberry Pi running headless Raspian 
    * ~~Raspberry Pi running headless Ubuntu for RPI~~ [COMPLETE] 
    * ~~Orange Pi 5+ running [Joshua Riek's Ubuntu distribution for Rockchip 3588 devices]** (https://github.com/Joshua-Riek/ubuntu-rockchip)~~[COMPLETE] 
    * ~~Orange Pi 3B running Armbian~~[COMPLETE] 
* Add FPS data to the Windows script(s) 
* CPU load per core 
* Fan speeds: desktop cases, desktop GPUs, individual fans on SBCs, fans in cluster cases 
* Find ways to get CPU clock speed and CPU and GPU temps on Windows and/or just possibly source data direct from AIDA64, or send the AIDA64 data to Grafana. 
* Ability to add an "activity flag" to the data, I.e., game vs machine learning on my Windows machine. 
* Use something like a Raspberry Pi Pico or to control case fans (for SBC cluster) depending on temperatures
* ~~Split the HW data scripts into separate versions for Linux and Windows, may need to do a separate one for Raspberry Pis as well.~~ [COMPLETE]

* **Update 10/24/2013:**
    * Put the scripts for different platforms in different directories, plus put all the tests in the same directory, also refactored the code for NVIDIA GPUs so the Linux and Windows scripts use the same script for running the NVIDIA SMI queries.

* **Update 10/13/2013:**
    * Added hardware scan script to get the names of that specific device's temperature sensors E.g. "SOC Thermal" for a Rockchip ARM64 device vs "Core Temp" on an Intel Device.
    * Added script and updated methods for retrieving data from an Orange Pi 5 Plus running a Rockship 3588 System on Chip (SOC), running [Joshua Rike's Ubuntu Distribution for Rockchip 3588x devices](https://github.com/Joshua-Riek/ubuntu-rockchip). This "should" work for the Armbian or other Linux distros available for this device, but I haven't tested it with those operating systems. 

* **Update 9/25/2023:** 
    * Added json config files for secrets + specifics like broker address, topics, etc., will make it easier to invoke these scripts from other applications, use on several machines, bash, PowerShelll scripts, etc., as you know pass all the important parameters via the command line. 
    * Added example JSON scripts 


* **Update 9/24/2023:** 
    * added scripts for Linux machines with GPU 
    * Light refactoring
    * Renamed files for consistency 


* **Update 9/21/2023: adding scripts for retrieving data on Windows machhines** 
    * Leveraged LibreHardwareMonitor for CPU temp and clock speeds on Windows - due to this requiring Admin rights to run the script, still looking into alternate methods of getting that data, especially since it's just two datapoints 
    * Used NVIDIA smi queries to retrieve GPU data - good part of this is I can re-use those queries on Linux devices with NVIDIA GPUs as well 
    * Short script for testing the NVIDIA SMI queries 
    * If you want to know more about NVIDIA SMI queries, you can read more [here](https://enterprise-support.nvidia.com/s/article/Useful-nvidia-smi-Queries-2)
    * Added GPU Power Draw to tracked metrics 

* **Update 9/18/2023: refactoring + improvements:**
    * streamlined the MQTT client and moved it to an external class that can be referenced from
any of the scripts being used to collect data. Removed the generic MQTT class as it's no longer needed with the existence utility class 
    * ClientIDs are now randomly generated, will use this in the future for some sort of onboarding/authentication process, but for now, a unique ID everytime the scripts are used 
    * Heavy refactor of the caseTemps and hardwareDataLinux scripts, (main method pattern), which should make creating/using unit tests in the future, external orchestration, etc., a lot easier. Also can use those as an easy template for dropping in other scripts, e.g., W11 data, Linux Devices with GPUs, Linux variants for Single Board ARM devices, etc. 
    * Added light logging of errors and exceptions 

* **Update 9/13/2023:** added generic MQTT client, separate scripts for Windows (pending) vs Linux devices without an NVIDIA GPU. 


#### Acknowledgements, shout-outs and the like 
* [The LibreHardwareMonitor Team - Repo](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor), which I used to monitor my W11 machine in instances the psutil or GPUutil wasn't able to access certaiin sensors on Windows
* I used [Matthieu Houdebine's Turing Smart Screen Repo](https://github.com/mathoudebine/turing-smart-screen-python) as a reference around how to use the LibreHardwareMonitor DLLs with Python 

#### Technical Details 
* Used a variety of machines given that a lot of the code is tailored towards certain devices, namely: 12th Gen i7 w/ NVIDIA 3090TI running W11, 12th Gen Intel NUC, Beelink SER5 Pro, Orange Pi 3B, 11th Gen i5 w/ 3060TI running Ubuntu 22.04, Orange Pi 5 Plus running [Joshua Riek's Ubuntu distribution for Rockchip 3588 devices](https://github.com/Joshua-Riek/ubuntu-rockchip) 
