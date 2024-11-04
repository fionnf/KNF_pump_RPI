// Pin definitions
#define PUMP_PIN1 9
#define PUMP_PIN2 10
#define SPEED_PIN1 A0  // Tacho pin for Pump 1
#define SPEED_PIN2 A1  // Tacho pin for Pump 2

// Variables to store RPM and pulse counts
volatile unsigned long count1 = 0;
volatile unsigned long count2 = 0;
unsigned long rpm1 = 0;
unsigned long rpm2 = 0;

const int updateInterval = 1000; // update interval for RPM calculation in ms
unsigned long previousMillis = 0;

// Initial pump duty cycle (adjust if needed for minimum speed requirement)
int initialDutyCycle = 50; // Adjust to an appropriate value

void setup() {
  Serial.begin(9600);

  // Set pump control pins to output
  pinMode(PUMP_PIN1, OUTPUT);
  pinMode(PUMP_PIN2, OUTPUT);

  // Set initial duty cycle for the pumps
  analogWrite(PUMP_PIN1, map(initialDutyCycle, 0, 100, 0, 255));
  analogWrite(PUMP_PIN2, map(initialDutyCycle, 0, 100, 0, 255));

  // Set up interrupts for tacho pins to count pulses
  pinMode(SPEED_PIN1, INPUT);
  pinMode(SPEED_PIN2, INPUT);
  attachInterrupt(digitalPinToInterrupt(SPEED_PIN1), ISR_count1, FALLING);
  attachInterrupt(digitalPinToInterrupt(SPEED_PIN2), ISR_count2, FALLING);
}

void loop() {
  // Calculate and print RPM every updateInterval milliseconds
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= updateInterval) {
    previousMillis = currentMillis;

    // Detach interrupts while calculating to ensure accurate counts
    detachInterrupt(digitalPinToInterrupt(SPEED_PIN1));
    detachInterrupt(digitalPinToInterrupt(SPEED_PIN2));

    // Calculate RPM (pulses per second * 60)
    rpm1 = count1 * (60000 / updateInterval);
    rpm2 = count2 * (60000 / updateInterval);

    // Print RPM values
    Serial.print("Pump 1 RPM: ");
    Serial.println(rpm1);
    Serial.print("Pump 2 RPM: ");
    Serial.println(rpm2);

    // Reset pulse counts for the next interval
    count1 = 0;
    count2 = 0;

    // Reattach interrupts
    attachInterrupt(digitalPinToInterrupt(SPEED_PIN1), ISR_count1, FALLING);
    attachInterrupt(digitalPinToInterrupt(SPEED_PIN2), ISR_count2, FALLING);
  }
}

// Interrupt service routines to count pulses
void ISR_count1() {
  count1++;
}

void ISR_count2() {
  count2++;
}