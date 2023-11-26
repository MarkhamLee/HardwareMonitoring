# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# quick and dirty script to test all the calls in the
# linux CPU data script for AMD devices

import os
import sys
# this allows us to import modules from the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from linux.linux_cpu_data import LinuxCpuData  # noqa: E402

get_data = LinuxCpuData()

# average clock speed for all cores
cpu_data, core_count = get_data.getFreq()
print(f'This machine has {core_count} total cores')
print(f'cpu freq is an average of: {cpu_data} over {core_count} cores')

# CPU load
cpu_util = get_data.getCPUData()
print(f'The CPU utilization is: {cpu_util}')

# get RAM usage
ram_util = get_data.getRamData()
print(f'Current RAM usage is: {ram_util}')


# get temps for AMD Device - CPU, GPU and NVME

nvme_temp, cpu_temp, amdgpu_temp = get_data.amd_linux_data()

temps = {
    "CPU Temp": cpu_temp,
    "GPU Temp": amdgpu_temp,
    "NVME Temp": nvme_temp
}

print(temps)
