import RPi.GPIO as GPIO
import time
import csv

# Configuration
pump_control_pin = 18  # GPIO pin for PWM control
frequency = 1000  # PWM frequency in Hz
duty_cycles = [2,5,10,15,20]  # Duty cycles to test
calibration_file = "calibration.csv"  # File to save calibration data
run_time = 30  # Time to run the pump at each duty cycle in seconds

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

        for duty_cycle in duty_cycles:
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

            # Brief pause before the next duty cycle
            time.sleep(2)

        print(f"Calibration complete. Data saved to {calibration_file}")

except KeyboardInterrupt:
    print("Calibration interrupted.")

finally:
    pwm.stop()
    GPIO.cleanup()