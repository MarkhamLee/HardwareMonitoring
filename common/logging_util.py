# Generic logging script
import logging
from sys import stdout


# set up/configure logging with stdout so it can be picked up by K8s
logger = logging.getLogger('hardware_telemetry')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')  # noqa: E501
handler.setFormatter(formatter)
logger.addHandler(handler)
