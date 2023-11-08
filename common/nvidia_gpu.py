# Markham Lee 2023
# Retrieving temp, load, etc., data from NVIDIA GPUs
# # https://github.com/MarkhamLee/HardwareMonitoring
# All the GPU data comes from NVIDI SMI Queries, you can read more here:
# https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
# this script is platform agnostic, should work exactly the same on Linux and
# Windows devices running x86 processors


import subprocess as sp


class NvidiaSensors():

    def __init__(self):

        pass

    # parsing the data from the smi query is fairly consistent, so created
    # this generalized query method I can either call directly with a query
    # or call via the other methods that have the "canned" queries already
    # set up.

    @staticmethod
    def smiParser(query: str):

        cmd = "nvidia-smi --query-gpu=" + query + " --format=csv,noheader"
        data = sp.check_output(cmd, shell=True)
        data = data.decode("utf-8").strip().split("\n")
        data = data[0]
        data = data.split(',')
        data = [''.join(x for x in i if x.isdigit()) for i in data]

        return data

    # getting all the data in one query saves on quite a bit of latency,
    # as whether it's one item or six, these queries run in about 30-40ms,
    # doing them separate it was closer to 250ms
    @staticmethod
    def gpuQuery():

        query = ("temperature.gpu,utilization.gpu,memory.used,power.draw,"
                 "clocks.current.graphics,encoder.stats.averageFps")

        data = NvidiaSensors.smiParser(query)

        # split out each value from the returned list of values

        temp = int(data[0])
        gpuLoad = int(data[1]) / 100
        gpuVram = round(((float(data[2])) / 1024), 2)
        gpuPower = round((float(data[3])) / 100, 2)
        gpuClock = int(data[4])

        # commented this out, as the FPS query shows the average across
        # all apps not useful for when I'm playing games. Will need to look
        # at an alternate approach like Riva Statistics Tuner. Also the
        # NVIDIA overlay app shows this data, so there is probably a way to
        # get this data via SMI queries that I just haven't discovered yet.
        # fps = int(data[5]) #

        return temp, gpuLoad, gpuVram, gpuPower, gpuClock

    # the following are the individual queries for the data points included in
    # the GPU query, I just put these here in case I needed them/needed to just
    # get an individual data point.
    @staticmethod
    def gpuLoad():

        query = "utilization.gpu"
        data = NvidiaSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def gpuTemp():

        query = "temperature.gpu"
        data = NvidiaSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def vramUsed():

        query = "memory.used"
        data = NvidiaSensors.smiParser(query)
        data = round((float(data[0]) / 1024), 2)

        return data

    @staticmethod
    def gpuPower():

        query = 'power.draw'
        data = NvidiaSensors.smiParser(query)
        data = round((float(data[0])) / 100, 2)

        return data

    @staticmethod
    def gpuFPS():

        query = 'encoder.stats.averageFps'
        data = NvidiaSensors.smiParser(query)
        data = int(data[0])

        return data

    @staticmethod
    def gpuClock():

        query = 'clocks.current.graphics'
        data = NvidiaSensors.smiParser(query)
        data = int(data[0])

        return data
