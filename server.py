import sys

from dotenv import load_dotenv
from usb import usb_monitor

def crtl_exit():
    sys.stdout.write('\r')
    print("Bye")
    sys.exit(0)

def server():
    usb_monitor.listen_usb()

if __name__ == '__main__':
    try:
        load_dotenv()
        server()
    except KeyboardInterrupt:
        crtl_exit()
