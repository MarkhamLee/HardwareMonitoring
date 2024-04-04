# Markham Lee (C) 2023
# Hardware Monitor for Linux & Windows:
# # https://github.com/MarkhamLee/HardwareMonitoring
# script to retrieve CPU related data, invoked by the script that
# communicate  with the MQTT broker.
# building this as a utility script so specific data can be grabbed,
# rather than having a single fuunction with all the data calls in it
import json
import psutil


class LinuxCpuData():

    def __init__(self):

        # get the # of cores, as we can use that to iterate through and
        # get things like current speed for all CPU cores
        self.core_count = psutil.cpu_count(logical=False)

    # for instances where we want to get data per core, we can pass the
    # function that retrieves that data to this one and then build the
    # "per core" payload
    def build_payload(self, inputFunction, index=0):

        temp_dict = {}

        while self.core_count > index:

            data = inputFunction[index].current
            data = round(data, 1)
            key = (f'core {index}')
            temp_dict[key] = data
            index += 1

        payload = json.dumps(temp_dict)

        return payload

    # getting temps per core
    def get_temps(self, index=0):

        if self.core_count > 1:

            temp_payload = self.build_payload(psutil.sensors_temperatures()
                                              ['coretemp'], index=0)

        else:
            core_temp = \
                psutil.sensors_temperatures()['coretemp'][index].current
            temp_payload = {'core 0': core_temp}
            temp_payload = json.dumps(temp_payload)

        return temp_payload

    # returns CPU package temp
    def core_temp(self):

        core_temp = psutil.sensors_temperatures()['coretemp'][0].current

        return core_temp

    # get average clock speed for all cores
    def get_freq(self, all_cpu=False):

        all_freq = psutil.cpu_freq(percpu=all_cpu)[0]
        all_freq = round(all_freq, 1)

        return all_freq, self.core_count

    # get frequency per core
    def freq_per_core(self, all_cpu=True):

        per_core_freq = self.build_payload(psutil.cpu_freq(percpu=all_cpu))

        return per_core_freq

    # CPU load
    def get_cpu_data(self):

        cpu_util = (psutil.cpu_percent(interval=1))
        cpu_util = round(cpu_util, 1)

        return cpu_util

    # get current RAM used
    def get_ram_data(self):

        ram_use = (psutil.virtual_memory()[3]) / 1073741824
        ram_use = round(ram_use, 2)

        return ram_use

    @staticmethod
    def amd_linux_data():

        nvme_temp = psutil.sensors_temperatures()['nvme'][0].current
        cpu_temp = psutil.sensors_temperatures()['k10temp'][0].current
        amdgpu_temp = psutil.sensors_temperatures()['amdgpu'][0].current

        return nvme_temp, cpu_temp, amdgpu_temp
