import os
import psutil
import pyudev
import sys
import time

from system.copy_files import find_files_to_copy
from system.copy_files import copy_to_localhost
from system.copy_files import copy_to_smb

def umount(mountpoint):
    if not os.system('umount '+ mountpoint):
        print('pode remover o pendrive! ...')
    else:
        raise Exception('Unable to umount usb drive')

def search_videos(mountpoint):
    qnt_files = int(input('Quantos arquivos foram criados?: '))
    return find_files_to_copy(mountpoint, qnt_files)

def copy_files(files, dst):
    if 'local' == dst:
        return copy_to_localhost(files)
    elif 'smb' == dst:
        return copy_to_smb(files)
    else:
        raise Exception('Invalid copy option')

def send_customer_videos(action, device):
    time.sleep(1)
    for p in psutil.disk_partitions():
        if p.device in device.device_node:
            print('Diretório encontrado: {} ...'.format(p.mountpoint))
            files = search_videos(p.mountpoint)
            dst = copy_files(files, 'local')
            umount(p.mountpoint)

def listen_usb():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')

    try:
        observer = pyudev.MonitorObserver(monitor, send_customer_videos)
        observer.start()
    except:
        print("Unexpected error: ", sys.exc_info()[0])
        observer.stop()

    while True:
        time.sleep(60 * 60 * 24)
