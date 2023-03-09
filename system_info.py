import platform
import sysconfig

import psutil
import time
import datetime
from pyspectator.computer import Computer
from platform import uname
import os
import sys

__version__ = "0.12"


def correct_size(bts):
    size = 1024
    for item in ["B", "Kb", "Mb", "Gb", "Tb"]:
        if bts < size:
            return f"{bts:.2f}{item}"
        bts /= size


def get_system_info() -> dict:
    """
    :returns: dict with a lot system, processor, network, disks, ram information
    """

    info = dict()
    c = Computer()
    network = c.network_interface
    info['info'] = dict()
    info['info']['system_info'] = dict()
    info['info']['system_info'] = {'system': {'comp_name': uname().node,
                                              'os_name': f"{uname().system} {uname().release}",
                                              'version': uname().version,
                                              'arch': uname().machine,
                                              'uptime': c.uptime,
                                              'boot_time': c.boot_time,
                                              'python_version': c.python_version,
                                              'Unix_time': time.time(),
                                              'sys_time': str(datetime.datetime.now()),
                                              'windir': os.getenv("windir"),
                                              'COMSPEC': os.getenv("COMSPEC"),
                                              'HOMEPATH': os.getenv("HOMEPATH")},

                                   'processor': {'name': uname().processor,
                                                 'phisycal_core': psutil.cpu_count(logical=False),
                                                 'all_core': psutil.cpu_count(logical=True),
                                                 'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц"},

                                   'network': {'name': network.name,
                                               'ip': network.ip_address,
                                               'broadcast_address': network.broadcast_address,
                                               "subnet_mask": network.default_route},

                                   'ram': {'volume': correct_size(psutil.virtual_memory().total),
                                           'available': correct_size(psutil.virtual_memory().available),
                                           'used': correct_size(psutil.virtual_memory().used)}
                                   }

    info['info']['disks'] = dict()
    for partition in psutil.disk_partitions():
        partition_usage = psutil.disk_usage(partition.mountpoint)

        info['info']['disks'][partition.device] = dict()
        info['info']['disks'][partition.device] = {'file_system': partition.fstype,
                                                   'size_total': correct_size(
                                                       partition_usage.total),
                                                   'size_used': correct_size(
                                                       partition_usage.used),
                                                   'size_free': correct_size(
                                                       partition_usage.free),
                                                   'percent':
                                                       f'{partition_usage.percent}'}

    return info


if __name__ == "__main__":
    if platform.platform().startswith("Windows"):
        from pprint import pprint

        s = get_system_info()
        pprint(s)
    else:
        print("Only for Windows")
