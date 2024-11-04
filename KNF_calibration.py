import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

# Configuration
pump_control_pin = 18  # GPIO pin for PWM control of the pump
frequency = 1000  # PWM frequency in Hz
run_time = 30  # Time to run the pump at each duty cycle in seconds

# Ask user for the base name of the calibration file
base_name = input("Enter the base name for the calibration file: ")
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
calibration_file = f"{base_name}_{current_time}.csv"

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_control_pin, GPIO.OUT)

# Initialize PWM on the pump control pin
pwm = GPIO.PWM(pump_control_pin, frequency)
pwm.start(0)  # Start with 0% duty cycle (pump off)

try:
    with open(calibration_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Duty Cycle (%)", "Flow Rate (mL/min)"])  # Header

        while True:
            # Ask user for the duty cycle percentage
            duty_cycle = float(input("Enter the duty cycle (%) or '0' to finish: "))
            if duty_cycle == 0:
                break

            # Set the current PWM duty cycle
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"Running pump at {duty_cycle}% duty cycle for {run_time} seconds...")

            # Run the pump at the specified duty cycle for the designated time
            time.sleep(run_time)

            # Stop the pump by setting duty cycle to 0
            pwm.ChangeDutyCycle(0)
            print("Pump stopped. Please measure volume dispensed.")

            # Ask user to input the measured volume
            volume_dispensed = float(input(f"Enter the volume dispensed (mL) at {duty_cycle}% duty cycle: "))

            # Calculate the flow rate in mL/min
            flow_rate = (volume_dispensed / run_time) * 60  # Convert to mL/min

            # Record the duty cycle and flow rate in the CSV file
            writer.writerow([duty_cycle, flow_rate])
            print(f"Recorded: {duty_cycle}% duty cycle = {flow_rate:.2f} mL/min")

        print(f"Calibration complete. Data saved to {calibration_file}")

except KeyboardInterrupt:
    print("Calibration interrupted.")

finally:
    pwm.stop()
    GPIO.cleanup()