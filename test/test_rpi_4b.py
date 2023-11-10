# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# quick and dirty script to test all the calls in the
# linux CPU data script

import sys
import os

# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from linux.linux_cpu_data import LinuxCpuData  # noqa: E402

getData = LinuxCpuData()

# average clock speed for all cores
cpuData, coreCount = getData.getFreq()
print(f'This machine has {coreCount} total cores')
print(f'cpu freq is an average of: {cpuData} over {coreCount} cores')


# CPU load
cpu_util = getData.getCPUData()
print(f'The CPU utilization is: {cpu_util}')


# get RAM usage
ramUsed = getData.getRamData()
print(f'Current RAM usage is: {ramUsed}')


# CPU temperature
rpi_temp = getData.get_rpi_4b_temps()
print(f'Current CPU temperature is: {rpi_temp}')
