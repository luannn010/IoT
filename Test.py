import serial

import credentials

# Open the serial port
ser = serial.Serial('COM6', 9600)

# Read and print the serial data
while True:
    data = ser.readline().decode().strip()
    # print(data)
    line = data.split(',')
    flame_value = line[0].split(':')[1]
    smoke_value = line[1].split(':')[1]
    # print(Flame, Smoke)
    # ip_address = os.popen('''hostname -I''').readline().replace('\n', '').replace(',', '.')[:-1]
    # mac_address = os.popen('''type /sys/class/net/*/address''').readline().replace('\n', '').replace(',', '.')
    ip_address = credentials.get_network_info()[0]
    mac_address = credentials.get_network_info()[1] 
    # print(ip_address, mac_address, Flame, Smoke)
    attributes = {
        'ip_address': ip_address,
        'macaddress': mac_address
    }
    telemetry = {
        'flame_value': int(flame_value),
        'smoke_value': int(smoke_value)
    }

# Close the serial port
ser.close()
