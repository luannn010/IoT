ACCESS_TOKEN = "i17jsf46y9ql86eep0bt"
THINGSBOARD_SERVER = '101.173.168.30'
THINGSBOARD_PORT = 1883
import socket
import uuid

def get_network_info():
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

# Get and print the IP address and MAC address
ip_address, mac_address = get_network_info()

# ACCESS_TOKEN = "i17jsf46y9ql86eep0bt"





