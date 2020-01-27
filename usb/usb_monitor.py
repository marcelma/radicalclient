import os
import psutil
import pyudev
import sys
import time

from clients.get_informations import client_informations
from files.copy_files import copy_files, search_videos

def umount(mountpoint):
    if os.system('umount '+ mountpoint):
        raise Exception('Unable to umount usb drive')

def send_customer_videos(action, device):
    client  = {}
    time.sleep(1)
    for p in psutil.disk_partitions():
        if p.device in device.device_node:
            if bool(os.getenv('CLIENT_GET_INFORMATION')):
                client = client_informations()

            # print('Diretório encontrado: {} ...'.format(p.mountpoint))
            client['videos'] = search_videos(p.mountpoint)

            temp_dir = copy_files(client['videos'])

            umount(p.mountpoint)

            # TODO: post processing: Take fotos from video
            copy_files(client['videos'], temp_dir, client)

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
