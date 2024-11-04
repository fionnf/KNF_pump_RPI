import RPi.GPIO as GPIO
import time

# Pin configuration
pump_pin = 18  # GPIO pin for the pump control
speed_pin = 23  # GPIO pin for the pump speed input

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.setup(speed_pin, GPIO.IN)

try:
    while True:
        # Set the pump control pin to HIGH (5V)
        GPIO.output(pump_pin, GPIO.HIGH)
        print("Pump running")

        # Read the value of the speed pin
        speed_value = GPIO.input(speed_pin)
        print(f"Speed pin value: {speed_value}")

        # Wait for a short period before measuring again
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    GPIO.cleanup()  # Clean up GPIO settings