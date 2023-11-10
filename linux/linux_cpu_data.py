# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# https://github.com/MarkhamLee/hardware-monitor
# script to retrieve CPU related data, invoked by the script that
# communicate  with the MQTT broker.
# building this as a utility script so specific data can be grabbed,
# rather than having a single fuunction with all the data calls in it

import psutil
import json


class LinuxCpuData():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.coreCount = psutil.cpu_count(logical=False)

    # for instances where we want to get data per core, we can pass the
    # function that retrieves that data to this one and then build the
    # "per core" payload
    def buildPayload(self, inputFunction, index=0):

        tempDict = {}

        while self.coreCount > index:

            data = inputFunction[index].current
            data = round(data, 1)
            key = (f'core {index}')
            tempDict[key] = data
            index += 1

        payload = json.dumps(tempDict)

        return payload

    # getting temps per core
    def getTemps(self, index=0):

        if self.coreCount > 1:

            tempPayload = self.buildPayload(psutil.sensors_temperatures()
                                            ['coretemp'], index=0)

        else:
            coreTemp = psutil.sensors_temperatures()['coretemp'][index].current
            tempPayload = {'core 0': coreTemp}
            tempPayload = json.dumps(tempPayload)

        return tempPayload

    # returns CPU package temp
    def coreTemp(self):

        coreTemp = psutil.sensors_temperatures()['coretemp'][0].current

        return coreTemp

    # get average clock speed for all cores
    def getFreq(self, all_cpu=False):

        allFreq = psutil.cpu_freq(percpu=all_cpu)[0]
        allFreq = round(allFreq, 1)

        return allFreq, self.coreCount

    # get frequency per core
    def freqPerCore(self, all_cpu=True):

        perCoreFreq = self.buildPayload(psutil.cpu_freq(percpu=all_cpu))

        return perCoreFreq

    # CPU load
    def getCPUData(self):

        cpuUtil = (psutil.cpu_percent(interval=1))
        cpuUtil = round(cpuUtil, 1)

        return cpuUtil

    # get current RAM used
    def getRamData(self):

        ramUse = (psutil.virtual_memory()[3]) / 1073741824
        ramUse = round(ramUse, 2)

        return ramUse

    # acquiring temperature sensor data for Rockchip 3588 devices
    @staticmethod
    def sysTemps():

        socTemp = psutil.sensors_temperatures()['soc_thermal'][0].current
        bigCore0Temp = psutil.sensors_temperatures()['bigcore0_thermal'][0].\
            current
        bigCore1Temp = psutil.sensors_temperatures()['bigcore1_thermal'][0].\
            current
        littleCoreTemp = psutil.\
            sensors_temperatures()['littlecore_thermal'][0].current
        centerTemp = psutil.sensors_temperatures()['center_thermal'][0].current
        gpuTemp = psutil.sensors_temperatures()['gpu_thermal'][0].current
        npuTemp = psutil.sensors_temperatures()['npu_thermal'][0].current
        nvmeTemp = psutil.sensors_temperatures()['nvme'][0].current

        return socTemp, bigCore0Temp, bigCore1Temp, littleCoreTemp, \
            centerTemp, gpuTemp, npuTemp, nvmeTemp

    # CPU frequencies for the various cores of a Rockchip 3588 device
    @staticmethod
    def getRockChip3588Freqs():

        freq = psutil.cpu_freq(percpu=True)
        littleCore = freq[0].current
        bigCore0 = freq[1].current
        bigCore1 = freq[2].current

        return littleCore, bigCore0, bigCore1

    # get CPU temp for Raspberry Pi 4B
    @staticmethod
    def get_rpi_4b_temps():

        rpi_cpu_temp = psutil.sensors_temperatures()['cpu_thermal'][0].current

        return rpi_cpu_temp

    @staticmethod 
    def rockchip_3566_temps():
        
        return psutil.sensors_temperatures()['cpu_thermal'][0].current,\
            psutil.sensors_temperatures()['gpu_thermal'][0].current

    


    

