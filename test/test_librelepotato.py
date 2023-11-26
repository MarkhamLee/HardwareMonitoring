# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# quick and dirty script to test all the calls in the
# linux CPU data script for Libre Le Potato devices running the AML-S905X-CC
# chip

import os
import sys
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

# get temps for CPU & GPU
cpu_temp = getData.libre_lepotato_temps()

print(f'The cpu_temp is: {cpu_temp}')
