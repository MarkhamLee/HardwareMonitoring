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
from win32api import *
import subprocess as sp


class WindowsSensors():

    def __init__(self):

        # verify that the app is running with Admin permission
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            print("Error: attempted to run script without admin rights,\
                  please re-open your IDE or shell with admin rights\
                  and ty again")
            try:
                sys.exit(0)

            except:
                os._exit(0)

        clr.AddReference(os.getcwd() + '\\Librehardwaremonitor\\\
                         LibreHardwareMonitorLib.dll')
        clr.AddReference(os.getcwd() + '\\Librehardwaremonitor\\HidSharp.dll')

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
                if sensor.SensorType == self.Hardware.SensorType.Temperature and str(sensor.Name).startswith("Core Average"):
                    cpu_temp = round(float(sensor.Value), 1)
                if sensor.SensorType == self.Hardware.SensorType.Clock and str(sensor.Name).startswith("CPU Core #"):
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

    # parsing the data from the smi query is fairly consistent, so created
    # this generalized query method I can either call directly with a query
    # or call via the other methods that have the "canned" queries already
    # set up.
    @staticmethod
    def smiParser(query):

        cmd = "nvidia-smi --query-gpu=" + query + " --format=csv,noheader"
        data = sp.check_output(cmd, shell=True)
        data = data.decode("utf-8").strip().split("\n")
        data = data[0]
        data = data.split(',')
        data = [''.join(x for x in i if x.isdigit()) for i in data]

        return data

    # get average CPU load for all cores via the PSutil library
    @staticmethod
    def getCPUData():

        # CPU load
        cpu_util = (psutil.cpu_percent())/100
        cpu_util = round(cpu_util, 2)

        return cpu_util

    # getting all the data in one query saves on quite a bit of latency,
    # as whether it's one item or six, these queries run in about 30-40ms,
    # but doing them separately took closer to 250ms.
    @staticmethod
    def gpuQuery():

        data = WindowsSensors.smiParser('temperature.gpu,utilization.gpu,\
                                        memory.used,power.draw,clocks.current.graphics,\
                                        encoder.stats.averageFps')

        # split out each value from the returned list of values

        temp = int(data[0])
        gpuLoad = int(data[1])/100
        gpuVram = round(((float(data[2])) / 1024), 2)
        gpuPower = round((float(data[3]))/100, 2)
        gpuClock = int(data[4])
        # returns avg across all apps, commenting out until I can find a
        # better option
        # fps = int(data[5])

        return temp, gpuLoad, gpuVram, gpuPower, gpuClock

    @staticmethod
    def getRAM():

        # RAM usage
        ramUse = (psutil. virtual_memory()[3])/1073741824
        ramUse = round(ramUse, 2)

        return ramUse

    # the following are the individual queries for the data points included
    # in the GPU query, I just put these here in case I needed them/needed
    # to just get an individual data point.
    @staticmethod
    def gpuLoad():

        query = "utilization.gpu"
        data = WindowsSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def gpuTemp():

        query = "temperature.gpu"
        data = WindowsSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def vramUsed():

        query = "memory.used"
        data = WindowsSensors.smiParser(query)
        data = round((float(data[0])/1024), 2)

        return data

    @staticmethod
    def gpuPower():

        query = 'power.draw'
        data = WindowsSensors.smiParser(query)
        data = round((float(data[0]))/100, 2)

        return data

    @staticmethod
    def gpuFPS():

        query = 'encoder.stats.averageFps'
        data = WindowsSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def gpuClock():

        query = 'clocks.current.graphics'
        data = WindowsSensors.smiParser(query)
        data = int(data[0])

        return data
