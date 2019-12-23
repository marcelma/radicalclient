import psutil
import pyudev
import time

def send_customer_videos(action, device):
    time.sleep(1)
    for p in psutil.disk_partitions():
        if p.device in device.device_node:
            print('Mount Point: {0}'.format(p.mountpoint))

def listen_usb():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block', device_type='partition')

    observer = pyudev.MonitorObserver(monitor, send_customer_videos)
    observer.start()

    while True:
        time.sleep(60 * 60 * 24)
