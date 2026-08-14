import socket
import uuid

def get_hostname():
    return socket.gethostname()

def get_mac_address():
    mac = uuid.getnode()
    return ":".join(f"{(mac >> ele) & 0xff:02x}" for ele in range(40, -1, -8))