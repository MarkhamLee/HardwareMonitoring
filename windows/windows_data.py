# Markham Lee 2023
# Hardware Monitor for Windows & Linux
# https://github.com/MarkhamLee/hardware-monitor
# This program makes use of the LibreHardWareMonitor repo:
# https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/tree/master
# in particular two .dll hidsharp and LibreHardwareMonitorLib in order to
# retrieve CPU data (temperature and clock frequency) Also: hat tip to
# Matthew Houdebine's Turing Smart Screen repo for insights around how to
# implement with Python All the GPU data comes from NVIDI SMI Queries, you
# can read more here:
# https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries


import psutil
import os
import sys
import clr
import ctypes
from statistics import mean


class WindowsSensors():

    def __init__(self):

        # create paths for C# .dlls for retrieving CPU data
        libPath1 = ('\\Librehardwaremonitor\\'
                    'LibreHardwareMonitorLib.dll')
        libpath2 = ('\\Librehardwaremonitor\\HidSharp.dll')

        # verify that the app is running with Admin permission
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print("Error: attempted to run script without admin rights,\
                  please re-open your IDE or shell with admin rights\
                  and ty again")
            try:
                sys.exit(0)

            except:
                os._exit(0)

        # load C# dllls
        clr.AddReference(os.getcwd() + libPath1)
        clr.AddReference(os.getcwd() + libpath2)

        # You'll get a squiggly line or error indication for an unresolved
        # import, don't worry, it will work anyway
        from LibreHardwareMonitor import Hardware

        self.Hardware = Hardware

        # get handler
        self.getHandlers()

    def getHandlers(self):

        self.handler = self.Hardware.Computer()
        self.handler.IsCpuEnabled = True

    # we use Libre Hardware Monitor to get the two datapoints we can't get
    # with psutil on Windows: CPU frequency and CPU temp
    def getLibreData(self):

        self.handler.Open()

        # create variables
        cpuCount = 0
        bigFreq = []
        littleFreq = []

        for hw in self.handler.Hardware:
            for sensor in hw.Sensors:
                # Average CPU core temperature
                if sensor.SensorType == self.Hardware.SensorType.\
                    Temperature and str(sensor.Name).\
                        startswith("Core Average"):
                    cpu_temp = round(float(sensor.Value), 1)
                if sensor.SensorType == self.Hardware.\
                    SensorType.Clock and str(sensor.Name).\
                        startswith("CPU Core #"):
                    cpu_clock = round(float(sensor.Value), 2)
                    cpuCount += 1
                    if cpuCount < 8:
                        bigFreq.append(cpu_clock)

                    else:
                        littleFreq.append(cpu_clock)

        self.handler.Close()

        bigFreqMean = round(mean(bigFreq), 1)
        littleFreqMean = round(mean(littleFreq), 1)

        return bigFreqMean, littleFreqMean, cpu_temp

    # get average CPU load for all cores via the PSutil library
    @staticmethod
    def getCPUData():

        # CPU load
        cpu_util = (psutil.cpu_percent()) / 100
        cpu_util = round(cpu_util, 2)

        return cpu_util

    @staticmethod
    def getRAM():

        # RAM usage
        ramUse = (psutil. virtual_memory()[3]) / 1073741824
        ramUse = round(ramUse, 2)

        return ramUse
