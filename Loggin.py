import logging.handlers
import os
from tb_gateway_mqtt import TBDeviceMqttClient
import serial
import credentials

ACCESS_TOKEN = credentials.ACCESS_TOKEN
THINGSBOARD_SERVER = credentials.THINGSBOARD_SERVER
THINGSBOARD_PORT = credentials.THINGSBOARD_PORT

logging.basicConfig(level=logging.DEBUG)
client = None
ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=115200,
	parity="N",
	stopbits=1,
	bytesize=8
)
ser.isOpen();

# default blinking period
period = 1.0

# Read the serial for any message. If a message is received, read it byte-by-byte and return it.
def readSerial():
	out = None
	while ser.in_waiting > 0:
		out = ser.read()
	return out
   
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
def prepareData(msg):
	motion_active = msg.decode("utf-8")
	ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]
	mac_address = os.popen('''cat /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')

	attributes = {
		'ip_address': ip_address,
		'macaddress': mac_address
	}
	telemetry = {
		'motion_active': int(motion_active)
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
		# Only send data to the ThingsBoard if a message is sent via Serial.
		msg = readSerial()
		if (msg != None):
			attributes, telemetry = prepareData(msg)
			client.send_attributes(attributes)
			client.send_telemetry(telemetry)
   
if __name__=='__main__':
		main()
