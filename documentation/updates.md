### Updates

* **04/03/24**
    * Added GitHub Actions config for building the Docker image for collecting PC case data with a Raspberry Pi 4B 
    * Extensive refactoring and code clean-up, normalizing variables, streamling code where possible, etc.
    * Removed the code for the single board computers, as it's being maintained as part of my [Kubernetes Project](https://github.com/MarkhamLee/kubernetes-k3s-data-and-IoT-platform/tree/main/hardware_monitoring) and my [Data platform project](https://github.com/MarkhamLee/finance-productivity-iot-informational-weather-dashboard/tree/main/hardware_telemetry). That code has also been rebuilt to be deployed as Docker containers that continuously provide telemetry data, rather than scripts you run from the command line. 
    * Added script/firmware for PC case data collection with a Raspberry Pi Pico (Jan '24)

* **10/24/2013:**
    * Put the scripts for different platforms in different directories, plus put all the tests in the same directory, also refactored the code for NVIDIA GPUs so the Linux and Windows scripts use the same script for running the NVIDIA SMI queries.

* **10/13/2013:**
    * Added hardware scan script to get the names of that specific device's temperature sensors E.g., "SOC Thermal" for a Rockchip ARM64 device vs "Core Temp" on an Intel Device. 
    * Added script and updated methods for retrieving data from an Orange Pi 5 Plus running a Rockchip 3588 System on Chip (SOC), running [Joshua Rike's Ubuntu Distribution for Rockchip 3588x devices](https://github.com/Joshua-Riek/ubuntu-rockchip). This "should" work for the Armbian or other Linux distros available for this device, but I haven't tested it with those operating systems. 


* **Update 9/24/2023:** 
    * added scripts for Linux machines with GPU 
    * Light refactoring
    * Renamed files for consistency 

* **Update 9/21/2023: adding scripts for retrieving data on Windows machhines** 
    * Leveraged LibreHardwareMonitor for CPU temperature and clock speeds on Windows - due to this requiring Admin rights to run the script, still looking into alternate methods of getting that data, especially since it is just two datapoints  
    * Used NVIDIA SMI queries to retrieve GPU data - good part of this is I can re-use those queries on Linux devices with NVIDIA GPUs as well  
    * Short script for testing the NVIDIA SMI queries  
    * If you want to know more about NVIDIA SMI queries, you can read more [here](https://enterprise-support.nvidia.com/s/article/Useful-nvidia-smi-Queries-2) 
    * Added GPU power usage to tracked metrics  