// Include Libraries
#include "Arduino.h"

// Pin Definitions
#define Flame	A2
#define MQ5_5V_PIN_AOUT	A0
#define Buzzer 2

// Global variables and defines
const int flameThreshold = 1500; // Threshold value for flame sensor
const int smokeThreshold = 300; // Threshold value for smoke sensor

// object initialization

// Setup the essentials for your circuit to work. It runs first every time your circuit is powered with electricity.
void setup() 
{
    // Setup Serial which is useful for debugging
    // Use the Serial Monitor to view printed messages
    Serial.begin(9600);
    while (!Serial) ; // wait for serial port to connect. Needed for native USB

    
    pinMode(Buzzer, OUTPUT); // Set Buzzer pin as output
}

// Main logic of your circuit. It defines the interaction between the components you selected. After setup, it runs over and over again, in an eternal loop.
void loop() 
{
    int flameValue = analogRead(Flame);
    int smokeValue = analogRead(MQ5_5V_PIN_AOUT);
    
    Serial.print("Flame : ");
    Serial.print(flameValue);
    Serial.print(", Smoke : ");
    Serial.println(smokeValue);
    
    if (flameValue > flameThreshold || smokeValue > smokeThreshold) {
        digitalWrite(Buzzer, HIGH); // Turn on the Buzzer
    } else {
        digitalWrite(Buzzer, LOW); // Turn off the Buzzer
    }
    
    if (Serial.available()) {
        char input = Serial.read();
        if (input == 'S' || input == 's') {
            while (true) {
                // Stop the program execution
            }
        }
    }
    
    delay(1000); // delay for 1 second
}