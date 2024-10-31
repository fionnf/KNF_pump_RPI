import RPi.GPIO as GPIO
import time
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Pump control script for Raspberry Pi.")
parser.add_argument(
    "--pwm1", type=float, required=True, help="PWM duty cycle percentage (0-100%) for pump 1"
)
parser.add_argument(
    "--pwm2", type=float, required=True, help="PWM duty cycle percentage (0-100%) for pump 2"
)
parser.add_argument(
    "--pwm_pin1", type=int, default=18, help="GPIO pin number for PWM output for pump 1 (default: 18)"
)
parser.add_argument(
    "--pwm_pin2", type=int, default=19, help="GPIO pin number for PWM output for pump 2 (default: 19)"
)
parser.add_argument(
    "--frequency", type=int, default=1000, help="PWM frequency in Hz (default: 1000)"
)

args = parser.parse_args()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pwm_pin1, GPIO.OUT)
GPIO.setup(args.pwm_pin2, GPIO.OUT)

# Initialize PWM on the specified pins with the given frequency
pwm1 = GPIO.PWM(args.pwm_pin1, args.frequency)
pwm2 = GPIO.PWM(args.pwm_pin2, args.frequency)
pwm1.start(0)  # Start PWM with 0% duty cycle (pump off)
pwm2.start(0)  # Start PWM with 0% duty cycle (pump off)

try:
    while True:
        # Apply the PWM signal to the pumps
        pwm1.ChangeDutyCycle(args.pwm1)
        pwm2.ChangeDutyCycle(args.pwm2)

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm1.stop()  # Stop the PWM output for pump 1
    pwm2.stop()  # Stop the PWM output for pump 2
    GPIO.cleanup()  # Clean up GPIO settings