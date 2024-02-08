// PIR Sensor
// Author: Kristian Oqueli Ambrose
// This sketch is to be used alongside a device capable of reading serial data and sendijng MQTT messages.
#define PIN_PIR 2

const int signalDelay = 5000; // The amount of time for nothing to be detected by the PIR sensor before it sends a serial output to state the room is clear.
unsigned long lastDetected;	  // the time (millis) when the last movement was detected.
bool signalSent = false;

void setup()
{
	Serial.begin(115200);
	lastDetected = millis();
}

void loop()
{
	if (digitalRead(PIN_PIR) == HIGH)
	{
		if ((millis() - lastDetected) > signalDelay)
		{
			Serial.print(0x1);
		}
		lastDetected = millis();
		signalSent = false;
	}

	if ((millis() - lastDetected) > signalDelay && !signalSent)
	{
		Serial.print(0x0);
		signalSent = true;
	}
}
