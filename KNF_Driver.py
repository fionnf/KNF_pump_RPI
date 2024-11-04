import RPi.GPIO as GPIO
import time
import argparse
import logging
from datetime import datetime

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
    "--pwm_pin2", type=int, default=16, help="GPIO pin number for PWM output for pump 2 (default: 16)"
)
parser.add_argument(
    "--rpm_pin1", type=int, default=23, help="GPIO pin number for RPM input for pump 1 (default: 23)"
)
parser.add_argument(
    "--rpm_pin2", type=int, default=24, help="GPIO pin number for RPM input for pump 2 (default: 24)"
)
parser.add_argument(
    "--frequency", type=int, default=1000, help="PWM frequency in Hz (default: 1000)"
)

args = parser.parse_args()

# Disable GPIO warnings
GPIO.setwarnings(False)

# Clean up GPIO settings before setting up
GPIO.cleanup()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pwm_pin1, GPIO.OUT)
GPIO.setup(args.pwm_pin2, GPIO.OUT)
GPIO.setup(args.rpm_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(args.rpm_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM on the specified pins with the given frequency
pwm1 = GPIO.PWM(args.pwm_pin1, args.frequency)
pwm2 = GPIO.PWM(args.pwm_pin2, args.frequency)
pwm1.start(args.pwm1)  # Start PWM with the specified duty cycle
pwm2.start(args.pwm2)  # Start PWM with the specified duty cycle

# Variables to store RPM and pulse counts
rpm1 = 0
rpm2 = 0
count1 = 0
count2 = 0

# Interrupt service routines to count pulses
def rpm_callback1(channel):
    global count1
    count1 += 1

def rpm_callback2(channel):
    global count2
    count2 += 1

# Set up interrupts for RPM reading
try:
    GPIO.add_event_detect(args.rpm_pin1, GPIO.FALLING, callback=rpm_callback1)
    GPIO.add_event_detect(args.rpm_pin2, GPIO.FALLING, callback=rpm_callback2)
except RuntimeError as e:
    print(f"Error setting up GPIO event detection: {e}")
    GPIO.cleanup()
    exit(1)

# Set up logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"pump_log_{timestamp}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Log RPM values
try:
    while True:
        # Calculate RPM (assuming 1 pulse per revolution and 1 second interval)
        rpm1 = count1 * 60
        rpm2 = count2 * 60

        # Reset pulse counts
        count1 = 0
        count2 = 0

        # Log RPM values
        log_message = f"RPM1: {rpm1}, RPM2: {rpm2}"
        print(log_message)
        logging.info(log_message)

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm1.stop()  # Stop the PWM output for pump 1
    pwm2.stop()  # Stop the PWM output for pump 2
    GPIO.cleanup()  # Clean up GPIO settings