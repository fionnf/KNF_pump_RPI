#include <Arduino.h>
#include <TimerOne.h>

// Define pump control pins
#define PUMP_PIN1 9        // PWM pin for Pump 1
#define PUMP_PIN2 10       // PWM pin for Pump 2

// Pump duty cycle (0-255 for 0-100%)
int dutyCycle1 = 0;
int dutyCycle2 = 0;

void setup() {
  Serial.begin(9600);

  // Set pump control pins as outputs
  pinMode(PUMP_PIN1, OUTPUT);
  pinMode(PUMP_PIN2, OUTPUT);

  // Set a fixed PWM frequency
  Timer1.initialize(100);  // Set frequency to 10 kHz (100 microseconds period)
  Timer1.pwm(PUMP_PIN1, dutyCycle1);
  Timer1.pwm(PUMP_PIN2, dutyCycle2);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      // Pump a small bit on Pump 1
      dutyCycle1 = 128;  // Set to 50% duty cycle
      Timer1.pwm(PUMP_PIN1, dutyCycle1);
      delay(1000);       // Pump for 1 second
      dutyCycle1 = 0;    // Stop pumping
      Timer1.pwm(PUMP_PIN1, dutyCycle1);
    } else if (command == '2') {
      // Pump a small bit on Pump 2
      dutyCycle2 = 128;  // Set to 50% duty cycle
      Timer1.pwm(PUMP_PIN2, dutyCycle2);
      delay(1000);       // Pump for 1 second
      dutyCycle2 = 0;    // Stop pumping
      Timer1.pwm(PUMP_PIN2, dutyCycle2);
    }
  }
}