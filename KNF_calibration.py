import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime

# Configuration
pump_control_pin = 18  # GPIO pin for PWM control
frequency = 1000  # PWM frequency in Hz
run_time = 30  # Time to run the pump at each duty cycle in seconds
tolerance = 0.5  # Acceptable tolerance for the flow rate in mL/min
initial_duty_cycle = 5  # Initial duty cycle to start with
initial_step_size = 5  # Initial step size for duty cycle adjustments
min_step_size = 1  # Minimum step size for fine adjustments

# Ask user for the base name of the calibration file
base_name = input("Enter the base name for the calibration file: ")
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
calibration_file = f"{base_name}_{current_time}.csv"

# Ask user for the target flow rate
target_flow_rate = float(input("Enter the target flow rate (mL/min): "))

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

        duty_cycle = initial_duty_cycle
        step_size = initial_step_size
        while True:
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

            # Check if the flow rate is within the acceptable tolerance
            if abs(flow_rate - target_flow_rate) <= tolerance:
                print(f"Target flow rate of {target_flow_rate} mL/min achieved at {duty_cycle}% duty cycle.")
                break

            # Adjust the duty cycle based on the measured flow rate
            if flow_rate < target_flow_rate:
                duty_cycle += step_size
            else:
                duty_cycle -= step_size

            # Decrease the step size as the difference between the measured flow rate and the target flow rate decreases
            step_size = max(min_step_size, step_size / 2)

            # Brief pause before the next iteration
            time.sleep(2)

        print(f"Calibration complete. Data saved to {calibration_file}")

except KeyboardInterrupt:
    print("Calibration interrupted.")

finally:
    pwm.stop()
    GPIO.cleanup()