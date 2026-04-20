import os
import subprocess as sp


PI_KVM_SECRET = os.environ['FLUFFY_PIKVM_NODE0_SECRET']
PI_KVM_IP = os.environ['FLUFFY_PIKVM_NODE0_IP']

OFF_CMD = (f'curl -X POST -k -u admin:{PI_KVM_SECRET} https://{PI_KVM_IP}/api/atx/power?action=off')  # noqa: E501
OFF_CMD = (f'curl -X POST -k -u admin:{PI_KVM_SECRET} https://{PI_KVM_IP}/api/atx/power?action=off')  # noqa: E501

data = sp.check_output(OFF_CMD, shell=True)
