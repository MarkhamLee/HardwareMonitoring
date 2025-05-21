# Markham Lee 2023 - 2025
# Hardware Monitor for Windows & Linux
# # https://github.com/MarkhamLee/HardwareMonitoring
# This program makes use of the LibreHardWareMonitor repo:
# https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/tree/master
# in particular two .dll hidsharp and LibreHardwareMonitorLib in order to
# retrieve CPU data (temperature and clock frequency)
# The purpose of this script is to a) test the libre DLLs and to
# acquire the sensor names to incorporate into your main script
import clr
import ctypes
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from common.logging_util import log_file_logger  # noqa: E402

logger = log_file_logger('Sensor_list')


class GetWindowsSensorNames():

    def __init__(self):

        # create paths for C# .dlls for retrieving CPU data
        lib_path1 = ('\\Librehardwaremonitor\\'
                     'LibreHardwareMonitorLib.dll')
        lib_path2 = ('\\Librehardwaremonitor\\HidSharp.dll')

        # verify that the app is running with Admin permission
        if ctypes.windll.shell32.IsUserAnAdmin() == 0:
            logger.info("Error: attempted to run script without admin rights,\
                        please re-open your IDE or shell with admin rights\
                        and ty again")
            try:
                sys.exit(0)

            except Exception as e:
                logger.debug(f'sys.exit(0) failed with error: {e} trying os._exit(0) instead')  # noqa: E501
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
    def get_libre_sensor_labels(self):

        self.handler.Open()

        for hw in self.handler.Hardware:
            for sensor in hw.Sensors:
                name = str(sensor.Name)
                type = str(sensor.SensorType)
                value = round(float(sensor.Value), 1)
                logger.info(f'The sensor type is: {type}, sensor name is: {name} and the returned value is: {value}')  # noqa: E501

        self.handler.Close()
