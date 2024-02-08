ACCESS_TOKEN_E1 = "i17jsf46y9ql86eep0bt"
ACCESS_TOKEN_E2 = "HENF2KKB4QP3bZlWoj5w"
ACCESS_TOKEN_E3 = "uIZPPZ22BIJbDD1bqC1L"
THINGSBOARD_SERVER = '101.173.168.30'
THINGSBOARD_PORT = 1883
import socket
import uuid
import os

def get_network_info_Windows():
    try:
        # Get the hostname of the system
        hostname = socket.gethostname()

        # Get the IP address corresponding to the hostname
        ip_address = socket.gethostbyname(hostname)

        # Get the MAC address
        mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(5, -1, -1)])

        return ip_address, mac_address
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    
    
def get_network_info_Linux():
    try:
        # Get the IP address
        ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]

        # Get the MAC address
        mac_address = os.popen('''cat /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')

        return ip_address, mac_address
    except Exception as e:
        print(f"Error: {e}")
        return None, None
    
def get_network_info_MacOS():
    try:
        # Get the IP address
        ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]

        # Get the MAC address
        mac_address = os.popen('''ifconfig en0 | awk '/ether/{print $2}' ''').readline().replace('\n', '').replace(',', '.')

        return ip_address, mac_address
    except Exception as e:
        print(f"Error: {e}")
        return None, None





