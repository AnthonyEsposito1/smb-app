# python standard library
from socket import socket, AF_INET, SOCK_STREAM, getfqdn
import socket as soc
import struct
# nmb
from nmb.NetBIOS import NetBIOS


def get_default_gateway_linux():
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue
            return soc.inet_ntoa(struct.pack("<L", int(fields[2], 16)))


def find_ip_name():
    network = get_default_gateway_linux()
    network = network.rsplit('.', 1)
    network = str(network[0]) + '.'
    ip_name = {}
    for ip in range(1, 256):
        addr = network + str(ip)
        s = socket(AF_INET, SOCK_STREAM)
        s.settimeout(0.01)
        if not s.connect_ex((addr, 139)):
            s.close()
            conn = NetBIOS()
            ip_name[conn.queryIPForName(addr)[0]] = addr
            conn.close()
        s.close()
    ip_name_list = [(v, k) for k, v in ip_name.items()]
    return ip_name_list

