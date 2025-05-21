# Markham Lee 2023 - 2025
# Hardware Monitor for Windows & Linux
# # https://github.com/MarkhamLee/HardwareMonitoring
# This program makes use of the LibreHardWareMonitor repo:
# https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/tree/master
# in particular two .dll hidsharp and LibreHardwareMonitorLib in order to
# retrieve CPU data (temperature and clock frequency) Also: hat tip to
# Matthew Houdebine's Turing Smart Screen repo:
# https://github.com/mathoudebine/turing-smart-screen-python/tree/main
# for insights around how to implement Libre Hardware Monitor within
# Python. All the GPU data comes from NVIDI SMI Queries, you
# can read more here:
# https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
import clr
import ctypes
import os
import psutil
import sys
from statistics import mean

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.logging_util import console_logging  # noqa: E402

logger = console_logging('windows_data_logging')


class WindowsSensors():

    def __init__(self):

        # create paths for C# .dlls for retrieving CPU data
        lib_path1 = ('\\Librehardwaremonitor\\'
                     'LibreHardwareMonitorLib.dll')
        lib_path2 = ('\\Librehardwaremonitor\\HidSharp.dll')

        # verify that the app is running with Admin permission
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            logger.debug("Error: attempted to run script without admin rights,\
                         please re-open your IDE or shell with admin rights\
                         and ty again")
            try:
                sys.exit(0)

            except Exception as e:
                logger.debug(f'Shutdown command sys.exit(0) failed with error: {e}, trying os.exit(0)')  # noqa: E501
                os._exit(0)

        # load C# dllls
        clr.AddReference(os.getcwd() + lib_path1)
        clr.AddReference(os.getcwd() + lib_path2)

        # You'll get a squiggly line or error indication for an unresolved
        # import, don't worry, it will work anyway
        from LibreHardwareMonitor import Hardware

        self.Hardware = Hardware

        # get handler
        self.get_handlers()

    def get_handlers(self):

        self.handler = self.Hardware.Computer()
        self.handler.IsCpuEnabled = True

    # we use Libre Hardware Monitor to get the two datapoints we can't get
    # with psutil on Windows: CPU frequency and CPU temp
    def get_libre_data(self):

        self.handler.Open()

        # create variables
        cpu_count = 0
        big_freq = []
        little_freq = []

        for hw in self.handler.Hardware:
            for sensor in hw.Sensors:
                # Average CPU core temperature
                if sensor.SensorType == self.Hardware.SensorType.\
                    Temperature and str(sensor.Name).\
                        startswith("CPU Core"):
                    cpu_temp = round(float(sensor.Value), 1)
                if sensor.SensorType == self.Hardware.\
                    SensorType.Clock and str(sensor.Name).\
                        startswith("CPU Core #"):
                    cpu_clock = round(float(sensor.Value), 2)
                    cpu_count += 1
                    if cpu_count < 8:
                        big_freq.append(cpu_clock)

                    else:
                        little_freq.append(cpu_clock)

        self.handler.Close()

        big_freq_mean = round(mean(big_freq), 1)
        little_freq_mean = round(mean(little_freq), 1)

        return big_freq_mean, little_freq_mean, cpu_temp

    # get average CPU load for all cores via the PSutil library
    @staticmethod
    def get_cpu_data():

        # CPU load
        cpu_util = (psutil.cpu_percent()) / 100
        cpu_util = round(cpu_util, 2)

        return cpu_util

    @staticmethod
    def get_ram():

        # RAM usage
        ram_use = (psutil. virtual_memory()[3]) / 1073741824
        ram_use = round(ram_use, 2)

        return ram_use
