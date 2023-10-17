# Markham Lee (C) 2023 
# Built this primarily for ARM64 CPUs and System on Chip (SOC) machines like Orange Pi 5/5+ 
# and Raspberry Pi, in addition to AMD machines, but it will work for Intel as well. The idea
# was to get the name of temperature sensors on non Intel machines that don't use names like 
# 'CPU Package" it just checks for the available temperature sensors and then drops that
# data into a file, which you can use a reference or use a modified version of it as a
# config file and just grab the sensor data you want. 


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





