#include <DHT.h>

#define DHTPIN 2          // Pin where the DHT22 is connected
#define DHTTYPE DHT22     // DHT type (DHT11 or DHT22)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(5000);  // Wait for 5 seconds between readings

  float temperature = dht.readTemperature();  // Read temperature in Celsius

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");
}
