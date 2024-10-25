import RPi.GPIO as GPIO
import time
import csv

# Configuration
pump_control_pin = 18  # GPIO pin for PWM control
frequency = 1000  # PWM frequency in Hz
min_duty_cycle = 10  # Minimum PWM duty cycle to start calibration
max_duty_cycle = 100  # Maximum PWM duty cycle to end calibration
step = 10  # Step size for PWM duty cycle increments
calibration_file = "calibration.csv"  # File to save calibration data
run_time = 30  # Time to run the pump at each duty cycle in seconds

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_control_pin, GPIO.OUT)

# Initialize PWM on the pump control pin
pwm = GPIO.PWM(pump_control_pin, frequency)
pwm.start(0)

try:
    with open(calibration_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Duty Cycle (%)", "Flow Rate (mL/min)"])  # Header

        for duty_cycle in range(min_duty_cycle, max_duty_cycle + 1, step):
            # Set the current PWM duty cycle
            pwm.ChangeDutyCycle(duty_cycle)
            print(f"Running pump at {duty_cycle}% duty cycle for {run_time} seconds...")

            # Wait for the specified run time
            time.sleep(run_time)

            # Ask user to input the measured volume
            volume_dispensed = float(input(f"Enter the volume dispensed (mL) at {duty_cycle}% duty cycle: "))

            # Calculate the flow rate in mL/min
            flow_rate = (volume_dispensed / run_time) * 60  # Convert to mL/min

            # Record the duty cycle and flow rate in the CSV file
            writer.writerow([duty_cycle, flow_rate])
            print(f"Recorded: {duty_cycle}% duty cycle = {flow_rate:.2f} mL/min")

            # Wait briefly before moving to the next step
            time.sleep(1)

        print(f"Calibration complete. Data saved to {calibration_file}")

except KeyboardInterrupt:
    print("Calibration interrupted.")

finally:
    pwm.stop()
    GPIO.cleanup()