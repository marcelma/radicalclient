import sys

from system import usb_monitor

def crtl_exit():
    sys.stdout.write('\r')
    print("Bye")
    sys.exit()

def server():
    usb_monitor.listen_usb()

if __name__ == '__main__':
    try:
        server()
    except KeyboardInterrupt:
        crtl_exit()
