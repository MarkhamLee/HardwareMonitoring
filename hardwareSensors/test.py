# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# quick and dirty script to test all the calls in the
# linux CPU data script


from linuxDataCPU import LinuxCpuData

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


# get CPU temperature per core
temps = getData.getTemps()
print(f'The per core CPU temps are: {temps}')

# Get package temp
temperature = getData.coreTemp()
print(f'The CPU package temp is: {temperature}')

# get clock speed per core
allClocks = getData.freqPerCore()
print(f'CPU clock speeds per core are as follows: {allClocks}')
