import RPi.GPIO as GPIO
import time
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Pump control script for Raspberry Pi.")
parser.add_argument(
    "--pwm", type=float, required=True, help="PWM duty cycle percentage (0-100%) determined by calibration"
)
parser.add_argument(
    "--pwm_pin", type=int, default=18, help="GPIO pin number for PWM output (default: 18)"
)
parser.add_argument(
    "--frequency", type=int, default=1000, help="PWM frequency in Hz (default: 1000)"
)

args = parser.parse_args()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pwm_pin, GPIO.OUT)

# Initialize PWM on the specified pin with the given frequency
pwm = GPIO.PWM(args.pwm_pin, args.frequency)
pwm.start(0)  # Start PWM with 0% duty cycle (pump off)

try:
    while True:
        # Apply the PWM signal to the pump
        pwm.ChangeDutyCycle(args.pwm_percent)

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm.stop()  # Stop the PWM output
    GPIO.cleanup()  # Clean up GPIO settings