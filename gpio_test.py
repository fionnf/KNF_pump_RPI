import RPi.GPIO as GPIO
import time

# Clean up GPIO settings at the start
GPIO.cleanup()

# Pin configuration
pump_pin = 18  # GPIO pin for the pump control
speed_pin = 23  # GPIO pin for the pump speed input

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.setup(speed_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to store pulse count and frequency
pulse_count = 0
frequency = 0

# Interrupt service routine to count pulses
def pulse_callback(channel):
    global pulse_count
    pulse_count += 1

# Set up interrupt on the speed pin
GPIO.add_event_detect(speed_pin, GPIO.FALLING, callback=pulse_callback)

try:
    while True:
        # Set the pump control pin to HIGH (5V)
        GPIO.output(pump_pin, GPIO.HIGH)
        print("Pump running")

        # Measure the frequency of the pulses
        pulse_count = 0
        time.sleep(1)  # Measure for 1 second
        frequency = pulse_count  # Frequency in Hz (pulses per second)
        print(f"Pump speed frequency: {frequency} Hz")

        # Wait for a short period before measuring again
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    GPIO.cleanup()  # Clean up GPIO settings