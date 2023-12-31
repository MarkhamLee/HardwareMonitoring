# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# simple script for testing all the NVIDIA SMI queries
# the SMI query script is platform agnostic, so this test
# works on both Linux and Windows devices running x86 processors

import os
import sys

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.nvidia_gpu import NvidiaSensors  # noqa: E402

getData = NvidiaSensors()


print('------------------Single query for all data------------------')

# test query that retreives all data in one query
temp, gpuLoad, gpuVram, gpuPower, gpuClock = getData.gpuQuery()

# results
print(f'GPU temp is: {temp}')
print(f'GPU load is: {gpuLoad}')
print(f'GPU RAM usage is: {gpuVram}')
print(f'Current GPU Power Consumption: {gpuPower}')
print(f'The current GPU clock speed (graphics shaders) is: {gpuClock}')
# commenting out for now, data isn't what I'd like
# E.g., FPS for the current game or video
# print(f'Current FPS is: {fps}')


print('------------------Individual Queries-------------------------')


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
# commenting out for now, data isn't what I'd like
# E.g., FPS for the current game or video
# print(f'Current FPS is: {fps}')
