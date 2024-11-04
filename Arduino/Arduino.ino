
// Pin definitions
#define PUMP_PIN1 9
#define PUMP_PIN2 10
#define SPEED_PIN1 A0
#define SPEED_PIN2 A1

// Variables to store pump speeds
int speed1 = 0;
int speed2 = 0;

// Variables to store raw analog values
int rawValue1 = 0;
int rawValue2 = 0;

void setup() {
  Serial.begin(9600);

  pinMode(PUMP_PIN1, OUTPUT);
  pinMode(PUMP_PIN2, OUTPUT);
  pinMode(SPEED_PIN1, INPUT);
  pinMode(SPEED_PIN2, INPUT);

  // Set initial pump speeds to 9% duty cycle
  analogWrite(PUMP_PIN1, map(9, 0, 100, 0, 255));
  analogWrite(PUMP_PIN2, map(9, 0, 100, 0, 255));
}

void loop() {
  // Read the raw analog values from the speed pins
  rawValue1 = analogRead(SPEED_PIN1);
  rawValue2 = analogRead(SPEED_PIN2);

  // Print the raw analog values
  Serial.print("Pump 1 raw value: ");
  Serial.println(rawValue1);
  Serial.print("Pump 2 raw value: ");
  Serial.println(rawValue2);

  // Wait for a short period before measuring again
  delay(1000);
}