#include <Arduino.h>

// Define pump control and tacho pins
#define PUMP_PIN1 9        // PWM pin for Pump 1
#define PUMP_PIN2 10       // PWM pin for Pump 2
#define TACHO_PIN1 A0      // Tacho pin for Pump 1 (using A0 for polling)
#define TACHO_PIN2 A1      // Tacho pin for Pump 2 (using A1 for polling)

// Variables to store pulse counts and RPM
volatile unsigned long count1 = 0;
volatile unsigned long count2 = 0;
unsigned long rpm1 = 0;
unsigned long rpm2 = 0;

// Pump duty cycle (0-255 for 0-100%)
int dutyCycle1 = 128;  // Adjust this value to set pump speed
int dutyCycle2 = 128;  // Adjust this value to set pump speed

const int updateInterval = 1000; // RPM update interval in ms
unsigned long previousMillis = 0;

// State variables for detecting edges
int lastState1 = HIGH;
int lastState2 = HIGH;

void setup() {
  Serial.begin(9600);

  // Set pump control pins as outputs
  pinMode(PUMP_PIN1, OUTPUT);
  pinMode(PUMP_PIN2, OUTPUT);

  // Set tacho pins as inputs
  pinMode(TACHO_PIN1, INPUT);
  pinMode(TACHO_PIN2, INPUT);

  // Set a fixed PWM frequency and initial duty cycle
  analogWriteFrequency(PUMP_PIN1, 10000);  // Set frequency to 10 kHz
  analogWriteFrequency(PUMP_PIN2, 10000);  // Set frequency to 10 kHz
  analogWrite(PUMP_PIN1, dutyCycle1);      // Set initial duty cycle for Pump 1
  analogWrite(PUMP_PIN2, dutyCycle2);      // Set initial duty cycle for Pump 2
}

void loop() {
  // Polling for falling edges on A0 and A1 to count pulses
  int currentState1 = digitalRead(TACHO_PIN1);
  int currentState2 = digitalRead(TACHO_PIN2);

  // Detect falling edge for Pump 1
  if (lastState1 == HIGH && currentState1 == LOW) {
    count1++;
  }
  lastState1 = currentState1;

  // Detect falling edge for Pump 2
  if (lastState2 == HIGH && currentState2 == LOW) {
    count2++;
  }
  lastState2 = currentState2;

  // Print the raw analog values in a continuous stream
  Serial.print(analogRead(TACHO_PIN1));
  Serial.print(",");
  Serial.println(analogRead(TACHO_PIN2));

  // Calculate RPM every updateInterval milliseconds
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= updateInterval) {
    previousMillis = currentMillis;

    // Calculate RPM based on pulse counts
    rpm1 = count1 * (60000 / updateInterval); // Pulses per minute for Pump 1
    rpm2 = count2 * (60000 / updateInterval); // Pulses per minute for Pump 2

    // Print RPM values to serial
    Serial.print("Pump 1 RPM: ");
    Serial.println(rpm1);
    Serial.print("Pump 2 RPM: ");
    Serial.println(rpm2);

    // Reset pulse counts for the next interval
    count1 = 0;
    count2 = 0;
  }
}