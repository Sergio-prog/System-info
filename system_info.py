import locale
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
from ctypes import windll

__version__ = "0.17b"


def correct_size(bts):
    size = 1024
    for item in ["B", "Kb", "Mb", "Gb", "Tb"]:
        if bts < size:
            return f"{bts:.2f}{item}"
        bts /= size


# TODO: fonts

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
    info['info']['system_info'] = {'system': {'Comp_name': uname().node,
                                              'OS_name': f"{uname().system} {uname().release}",
                                              'Version': uname().version,
                                              'Arch': uname().machine,
                                              'Uptime': c.uptime,
                                              'Boot_time': c.boot_time,
                                              'Python_version': c.python_version,
                                              'Unix_time': time.time(),
                                              'Sys_time': str(datetime.datetime.now()),
                                              'Timezone': datetime.datetime.now().astimezone().tzname(),
                                              'windir': os.getenv("windir"),
                                              'COMSPEC': os.getenv("COMSPEC"),
                                              'HOMEPATH': os.getenv("HOMEPATH"),
                                              'Screen width resolution': windll.user32.GetSystemMetrics(0),
                                              'Screen height resolution': windll.user32.GetSystemMetrics(1),
                                              'System language': locale.windows_locale[
                                                  windll.kernel32.GetUserDefaultUILanguage()]},

                                   'Processor': {'name': uname().processor,
                                                 'Physical_core': psutil.cpu_count(logical=False),
                                                 'All_core': psutil.cpu_count(logical=True),
                                                 'Freq_max': f"{psutil.cpu_freq().max:.2f}Мгц",
                                                 'Temperature': f"{cpu.temperature} °C",
                                                 'Load': f"{cpu.load} %"},

                                   'Network': {'name': network.name,
                                               'IP': network.ip_address,
                                               'Broadcast_address': network.broadcast_address,
                                               "Subnet_mask": network.default_route},

                                   'RAM': {'Volume': correct_size(psutil.virtual_memory().total),
                                           'Available': correct_size(psutil.virtual_memory().available),
                                           'Used': correct_size(psutil.virtual_memory().used)},

                                   'GPU': {'name': gpu.name,
                                           'ID': gpu.id,
                                           'Serial': gpu.serial,
                                           'uuid': gpu.uuid,
                                           'ram_volume': f"{gpu.memoryTotal} MB",
                                           'ram_available': f"{gpu.memoryFree} MB",
                                           'ram_used': f"{gpu.memoryUsed} MB",
                                           'Driver': gpu.driver,
                                           'Temperature': f"{gpu.temperature} °C",
                                           'Load': f"{gpu.load} %"},
                                   'Motherboard': {'name': mboard.Name,
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
