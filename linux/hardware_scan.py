# Markham Lee (C) 2023
# https://github.com/MarkhamLee/Hardware-Monitoring
# Built this primarily for ARM64 CPUs and System on Chip (SOC)
# machines like Orange Pi 5/5+ and Raspberry Pi 4B, in addition to AMD
# machines. However, but it will work for Intel machines as well. The
# idea was to get the name of temperature sensors on non Intel machines
# that don't use names like 'CPU Package. It just checks for the available
# temperature sensors and then writes the sensor names into a json file,
# which can be used as a reference or as the basis as config files.


import psutil
import json

# get the dictionary of all sensor data
tempDict = psutil.sensors_temperatures()

# filter out the keys
sensorList = list(tempDict.keys())

print(sensorList)

# save the keys as a json file
with open('config/scanOpi5_baseline.json', 'w') as f:
    json.dump(sensorList, f, indent=4)

print(psutil.cpu_freq(percpu=True))
