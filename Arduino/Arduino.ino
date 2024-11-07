#include <Arduino.h>
#include <TimerOne.h>

// Define pump control and tacho pins
#define PUMP_PIN1 10        // PWM pin for Pump 1
#define PUMP_PIN2 9         // PWM pin for Pump 2
#define TACHO_PIN1 A1       // Tacho pin for Pump 1 (using A0 for polling)
#define TACHO_PIN2 A0       // Tacho pin for Pump 2 (using A1 for polling)

// Variables to store pulse counts and RPM
volatile unsigned long count1 = 0;
volatile unsigned long count2 = 0;
unsigned long rpm1 = 0;
unsigned long rpm2 = 0;

// Pump duty cycle (0-255 for 0-100%)
int dutyCycle1 = 80;  // Adjust this value to set pump speed
int dutyCycle2 = 0;  // Adjust this value to set pump speed

const int updateInterval = 1000; // RPM update interval in ms
unsigned long previousMillis = 0;

// State variables for detecting edges
int lastState1 = HIGH;
int lastState2 = HIGH;

// Moving average filter parameters
const int filterSize = 25;
unsigned long rpm1Readings[filterSize] = {0};
unsigned long rpm2Readings[filterSize] = {0};
int filterIndex1 = 0;
int filterIndex2 = 0;
unsigned long rpm1Sum = 0;
unsigned long rpm2Sum = 0;

void setup() {
  Serial.begin(9600);

  // Set pump control pins as outputs
  pinMode(PUMP_PIN1, OUTPUT);
  pinMode(PUMP_PIN2, OUTPUT);

  // Set tacho pins as inputs
  pinMode(TACHO_PIN1, INPUT);
  pinMode(TACHO_PIN2, INPUT);

  // Set a fixed PWM frequency and initial duty cycle
  Timer1.initialize(100);  // Set frequency to 10 kHz (100 microseconds period)
  Timer1.pwm(PUMP_PIN1, dutyCycle1);
  Timer1.pwm(PUMP_PIN2, dutyCycle2);

  Serial.print("Pump 1 rpm");
  Serial.print(", ");
  Serial.print("Pump 1 avg");
  Serial.print(", ");
  Serial.print("Pump 2 rpm");
  Serial.print(", ");
  Serial.println("Pump 2 avg");

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

  // Calculate RPM every updateInterval milliseconds
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= updateInterval) {
    previousMillis = currentMillis;

    // Calculate RPM based on pulse counts
    rpm1 = count1 * (60000 / updateInterval); // Pulses per minute for Pump 1
    rpm2 = count2 * (60000 / updateInterval); // Pulses per minute for Pump 2

    // Update moving average filter for rpm1
    rpm1Sum -= rpm1Readings[filterIndex1];
    rpm1Readings[filterIndex1] = rpm1;
    rpm1Sum += rpm1Readings[filterIndex1];
    filterIndex1 = (filterIndex1 + 1) % filterSize;
    unsigned long rpm1Avg = rpm1Sum / filterSize;

    // Update moving average filter for rpm2
    rpm2Sum -= rpm2Readings[filterIndex2];
    rpm2Readings[filterIndex2] = rpm2;
    rpm2Sum += rpm2Readings[filterIndex2];
    filterIndex2 = (filterIndex2 + 1) % filterSize;
    unsigned long rpm2Avg = rpm2Sum / filterSize;

    // Print RPM values to serial in a format suitable for Serial Plotter
    Serial.print(rpm1);
    Serial.print(", ");
    Serial.print(rpm1Avg);
    Serial.print(", ");
    Serial.print(rpm2);
    Serial.print(", ");
    Serial.println(rpm2Avg);

    // Adjust duty cycle of Pump 2 to match RPM of Pump 1
    int rpmDifference = rpm1Avg - rpm2Avg;
    dutyCycle2 += rpmDifference / 200; // Adjust this factor as needed for how aggressive adjustments are
    dutyCycle2 = constrain(dutyCycle2, 0, 255);
    Timer1.pwm(PUMP_PIN2, dutyCycle2);

    // Reset pulse counts for the next interval
    count1 = 0;
    count2 = 0;
  }
}