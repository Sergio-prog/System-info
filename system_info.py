import platform

import psutil
import time
import datetime
from pyspectator.computer import Computer
from pyspectator.processor import Cpu
from platform import uname
import os
import GPUtil
import wmi

__version__ = "0.13c"


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
    gpu = GPUtil.getGPUs()[0]
    cpu = Cpu(2)
    mboard = wmi.WMI().Win32_BaseBoard()[0]
    bios = wmi.WMI().Win32_BIOS()[0]
    kb = wmi.WMI().Win32_Keyboard()[0]

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
                                                 'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц",
                                                 'temperature': f"{cpu.temperature} °C",
                                                 'load': f"{cpu.load} %"},

                                   'network': {'name': network.name,
                                               'ip': network.ip_address,
                                               'broadcast_address': network.broadcast_address,
                                               "subnet_mask": network.default_route},

                                   'ram': {'volume': correct_size(psutil.virtual_memory().total),
                                           'available': correct_size(psutil.virtual_memory().available),
                                           'used': correct_size(psutil.virtual_memory().used)},

                                   'gpu': {'name': gpu.name,
                                           'ID': gpu.id,
                                           'Serial': gpu.serial,
                                           'uuid': gpu.uuid,
                                           'ram_volume': f"{gpu.memoryTotal} MB",
                                           'ram_available': f"{gpu.memoryFree} MB",
                                           'ram_used': f"{gpu.memoryUsed} MB",
                                           'driver': gpu.driver,
                                           'temperature': f"{gpu.temperature} °C",
                                           'load': f"{gpu.load} %"},
                                   'motherboard': {'name': mboard.Name,
                                                   'Model': mboard.Model,
                                                   'product': mboard.Product,
                                                   'serial-number': mboard.SerialNumber},
                                   'BIOS': {'name': bios.name,
                                            'serial_number': bios.SerialNumber,
                                            'version': bios.version}
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
