# Markham Lee (C) 2023 
# Hardware Monitor for Linux & Windows: https://github.com/MarkhamLee/hardware-monitor
# simple script for testing all the NVIDIA SMI queries 

# just uncomment out the version you need. 

from linuxDataGPU import LinuxGPUSensors
#from windowsdata import WindowsSensors


#getData = WindowsSensors() 
getData = LinuxGPUSensors() 


print('-------------------------------Single query for all data-------------------------------')

# test query that retreives all data in one query 
temp, gpuLoad, gpuVram, gpuPower, gpuClock = getData.gpuQuery()

#results
print(f'GPU temp is: {temp}')
print(f'GPU load is: {gpuLoad}')
print(f'GPU RAM usage is: {gpuVram}')
print(f'Current GPU Power Consumption: {gpuPower}')
print(f'The current GPU clock speed (graphics shaders) is: {gpuClock}')
#print(f'Current FPS is: {fps}') commenting out for now, data isn't what I'd like E.g., FPS for the current game or video


print('-------------------------------Individual Queries--------------------------------------')


# test individual queries 
tempIndi = getData.gpuTemp()
print(f'GPU temp is {tempIndi}')

loadIndi = getData.gpuLoad()
print(f'GPU load is: {loadIndi}')

vramIndi = getData.vramUsed()
print(f'GPU RAM usage is: {vramIndi}')

powerIndi = getData.gpuPower()
print(f'Current GPU power consumption is: {powerIndi}')

clockIndi = getData.gpuClock()
print(f'The current GPU clock speed (graphics shaders) is: {clockIndi}')

# commenting out for now, data isn't what I'd like E.g., FPS for the current game or video
#fpsIndi = getData.getCPUData()
#print(f'The current FPS is: {fpsIndi}')

