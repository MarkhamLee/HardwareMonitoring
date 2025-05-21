## Setting up the Libre Hardware Libraries 

### Installation

* Download the latest version of the LibrehardwareMonitor from [here](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/tree/master), you'll want the version called: "LibreHardwareMonitorLib" as that contains the files you would use to integrate the LibreHardwareMonitor into another application.
* You'll need two DLL files that will be in the main directory after you unzip the files.
    * "HidSharp.dll" 
    * "LibreHardwareMonitorLib.dll"
* Once you have the files downloaded, you will likely need to go into file properties and click "unblock" so you can use the files, otherwise your script will throw an error when the python script tries to load the DLLs.
* Dependencies and packages:
    * Install the .NET depencies as indicated in the LibreHardwareMonitor Repo
    * You'll also need the following Python dependencies so that you can use the DLLs from within your Python script(s)
        * pythonnet==3.0.5 <- this one has the version of CLR you need, DO NOT install clr directly, it will be the wrong package
        * pywin32==306

### Testing & Troubleshooting
* Once you've gotten everything setup, run the data prototyping notebook to get a list of the available sensors. Note: the monitor_windows_gpu.py will likely work out of the box, BUT if it doesn't run the notebook to get the sensor names so you can see what sensors are available to you.
* If certain sensors (e.g., CPU temp) are missing, then it's likely that your motherboard isn't currently supported by the LibreHardwareMonitor library and/or that you just need to upgrade to the latest version. E.g., let's say you cloned this repo and you have a CPU & Motherboard that came out after the last time I added the most recent DLLs to this repo (May 20th, 2025) then it's likely that the library won't be able to pull data from all the available sensors. Updating the DLLs to the latest versions should resolve the issue. E.g., I ran into this issue with my Asus NUC 14 Performance mini desktop machine, I could get CPU voltage and load but not frequency and temperature, after updating to the latest DLLs and unblocking the files, things worked fine.

### Acknowledgements, license details and the like
* I've included the [license](https://github.com/MarkhamLee/HardwareMonitoring/blob/main/LICENSE) for these files per the instructions in the repo, if I got something wrong, let me know. 
