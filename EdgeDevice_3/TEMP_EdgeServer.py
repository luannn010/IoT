import serial
import time
import paho.mqtt.client as mqtt
import json
import os
import credentials

# Serial port for Arduino
device = '/dev/ttyS3'  

# ThingsBoard configuration
THINGSBOARD_SERVER = credentials.THINGSBOARD_SERVER
ACCESS_TOKEN = credentials.ACCESS_TOKEN_E3

# Open serial connection to Arduino
arduino = serial.Serial(device, 9600)

# Connect to ThingsBoard MQTT broker
mqttClient = mqtt.Client()
mqttClient.username_pw_set(ACCESS_TOKEN)
mqttClient.connect(THINGSBOARD_SERVER, 1883, 60)

# Set up logging
import logging
logging.basicConfig(level=logging.DEBUG)

def read_serial():
    out = None
    while arduino.in_waiting > 0:
        out = arduino.readline().decode('utf-8').strip()
    return out

# Prepares data to be sent to via MQTT to the ThingsBoard platform.
# Data is formatted as a JSON string.
def prepare_data(msg):
    temperature_str = msg.split(' ')[1]
    temperature = float(temperature_str)

    ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]
    mac_address = os.popen('''cat /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')

    data = {
        'ip_address': ip_address,
        'macaddress': mac_address,
        'temperature': temperature
    }
    return json.dumps(data)

try:
    while True:
        # Read temperature from Arduino
        arduino_data = read_serial()
        
        if arduino_data:
            print(f"Temperature: {arduino_data} °C")
            
            # Prepare data for ThingsBoard
            payload = prepare_data(arduino_data)

            # Publish telemetry data to ThingsBoard
            mqttClient.publish("v1/devices/me/telemetry", payload, qos=1)
            
        # Delay for a moment to avoid overwhelming the Arduino
        time.sleep(1)

except KeyboardInterrupt:
    print("Script terminated by user.")

finally:
    # Close the serial connection and MQTT connection
    arduino.close()
    mqttClient.disconnect()
    print("Connections closed.")
