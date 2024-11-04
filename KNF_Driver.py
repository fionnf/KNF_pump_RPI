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
    "--rpm_pin1", type=int, default=23, help="GPIO pin number for RPM input for pump 1"
)
parser.add_argument(
    "--rpm_pin2", type=int, default=24, help="GPIO pin number for RPM input for pump 2"
)
parser.add_argument(
    "--frequency", type=int, default=1000, help="PWM frequency in Hz (default: 1000)"
)

args = parser.parse_args()

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pwm_pin1, GPIO.OUT)
GPIO.setup(args.pwm_pin2, GPIO.OUT)
GPIO.setup(args.rpm_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(args.rpm_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM on the specified pins with the given frequency
pwm1 = GPIO.PWM(args.pwm_pin1, args.frequency)
pwm2 = GPIO.PWM(args.pwm_pin2, args.frequency)
pwm1.start(0)  # Start PWM with 0% duty cycle (pump off)
pwm2.start(0)  # Start PWM with 0% duty cycle (pump off)

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
GPIO.add_event_detect(args.rpm_pin1, GPIO.FALLING, callback=rpm_callback1)
GPIO.add_event_detect(args.rpm_pin2, GPIO.FALLING, callback=rpm_callback2)

# Set up logging
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"pump_log_{timestamp}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')

# Control loop to adjust PWM duty cycle based on RPM difference
try:
    integral_error = 0
    previous_error = 0
    Kp = 0.1  # Proportional gain
    Ki = 0.01  # Integral gain

    while True:
        # Calculate RPM (assuming 1 pulse per revolution and 1 second interval)
        rpm1 = count1 * 60
        rpm2 = count2 * 60

        # Reset pulse counts
        count1 = 0
        count2 = 0

        # Calculate error and integral of error
        error = rpm1 - rpm2
        integral_error += error

        # Adjust PWM duty cycle to keep RPMs as close as possible
        adjustment = Kp * error + Ki * integral_error
        pwm1.ChangeDutyCycle(max(0, min(100, args.pwm1 - adjustment)))
        pwm2.ChangeDutyCycle(max(0, min(100, args.pwm2 + adjustment)))

        # Print and log RPM values for debugging
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