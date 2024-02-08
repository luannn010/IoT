import logging.handlers
from tb_gateway_mqtt import TBDeviceMqttClient
import credentials
import random
import time

ACCESS_TOKEN = credentials.ACCESS_TOKEN_E1
THINGSBOARD_SERVER = credentials.THINGSBOARD_SERVER
THINGSBOARD_PORT = credentials.THINGSBOARD_PORT
    
# In case using Windows Edge Device 
ip_address, mac_address = credentials.get_network_info_Windows()
# In case using Linux Edge Device
# ip_address, mac_address = credentials.get_network_info_Linux()
# In case using MacOS Edge Device

logging.basicConfig(level=logging.DEBUG)
client = None

# default blinking period
period = 1.0


# callback function that will call when we will send RPC
def rpc_callback(id, request_body):
    # request body contains method and other parameters
    print(request_body)
    method = request_body.get('method')
    if method == 'getTelemetry':
        attributes, telemetry = prepareData()
        client.send_attributes(attributes)
        client.send_telemetry(telemetry)
    else:
        print('Unknown method: ' + method)

# Prepares data to be sent to via MQTT to the ThingsBoard platform.
# Data is formatted as a JSON string.
# This implementation currently only takes a singly byte as the message, which is passed into the motion_active variable.
def prepareData():
    
    flame_value = random.randint(900, 1250)
    smoke_value = random.randint(80, 110)

    attributes = {
        'ip_address': ip_address,
        'macaddress': mac_address
    }
    telemetry = {
        'flame_value': flame_value,
        'smoke_value': smoke_value
    }
    print(attributes, telemetry)
    return attributes, telemetry


# request attribute callback
def sync_state(result, exception=None):
    global period
    if exception is not None:
        print("Exception: " + str(exception))
    else:
        period = result.get('shared', {'blinkingPeriod': 1.0})['blinkingPeriod']

def main():
    global client
    client = TBDeviceMqttClient(THINGSBOARD_SERVER, THINGSBOARD_PORT, ACCESS_TOKEN)
    client.connect()
    client.request_attributes(shared_keys=['blinkingPeriod'], callback=sync_state)
    
    # now rpc_callback will process rpc requests from server
    client.set_server_side_rpc_request_handler(rpc_callback)

    while not client.stopped:
        # Simulate data from a source
        
        attributes, telemetry = prepareData()
        client.send_attributes(attributes)
        client.send_telemetry(telemetry)
        time.sleep(1)     
if __name__ == '__main__':
    main()
