import os
import psutil
import pyudev
import sys
import time

from clients.get_informations import client_informations
from files.copy_files import copy_to_localhost
from files.copy_files import copy_to_smb
from files.copy_files import find_files_to_copy

def umount(mountpoint):
    if os.system('umount '+ mountpoint):
        raise Exception('Unable to umount usb drive')

def search_videos(mountpoint):
    qnt_files = int(input('Quantos arquivos foram criados?: '))
    return find_files_to_copy(mountpoint, qnt_files)

def copy_files(files, orig_dir=None, client=None):
    if not orig_dir:
        return copy_to_localhost(files)
    elif orig_dir:
        return copy_to_smb(files, orig_dir, client)
    else:
        raise Exception('Invalid copy option')

def send_customer_videos(action, device):
    client  = {}
    time.sleep(1)
    for p in psutil.disk_partitions():
        if p.device in device.device_node:
            if bool(os.getenv('CLIENT_GET_INFORMATION')):
                client = client_informations()

            print('Diretório encontrado: {} ...'.format(p.mountpoint))
            client['videos'] = search_videos(p.mountpoint)

            orig_dir = copy_files(client['videos'])

            umount(p.mountpoint)

            # TODO: post processing: Take fotos from video
            copy_files(client['videos'], orig_dir, client)

            print('pode remover o pendrive! ...')

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
