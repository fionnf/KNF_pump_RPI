import RPi.GPIO as GPIO
import time
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Pump control script for Raspberry Pi.")
parser.add_argument(
    "--flow_rate", type=float, default=100, help="Desired flow rate in mL/min (default: 100)"
)
parser.add_argument(
    "--model", type=str, choices=["KP", "KT"], default="KP", help="Pump model type: KP or KT (default: KP)"
)
parser.add_argument(
    "--pwm_pin", type=int, default=18, help="GPIO pin number for PWM output (default: 18)"
)
parser.add_argument(
    "--frequency", type=int, default=1000, help="PWM frequency in Hz (default: 1000)"
)

args = parser.parse_args()

# Map model type to slope values
model_slopes = {
    "KP": 33.33,  # KP model: 0.5V = 0 mL/min, 5V = 150 mL/min
    "KT": 28.89,  # KT model: 0.5V = 0 mL/min, 5V = 130 mL/min
}

# Calculate the PWM value based on the flow rate and model
def calculate_pwm_value(flow_rate, model):
    slope = model_slopes[model]  # Select the correct slope based on model

    # Calculate control voltage based on desired flow rate
    control_voltage = (flow_rate / slope) + 0.5

    # Ensure control voltage is within the range 0.5V to 5V
    if control_voltage > 5.0:
        control_voltage = 5.0
    if control_voltage < 0.5:
        control_voltage = 0.5

    # Convert control voltage to PWM duty cycle (0-100%)
    pwm_value = (control_voltage - 0.5) * (100.0 / 4.5)  # Convert to % for GPIO PWM
    return pwm_value

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(args.pwm_pin, GPIO.OUT)

# Initialize PWM on the specified pin with the given frequency
pwm = GPIO.PWM(args.pwm_pin, args.frequency)
pwm.start(0)  # Start PWM with 0% duty cycle (pump off)

try:
    while True:
        # Calculate the PWM value for the desired flow rate and model type
        pwm_value = calculate_pwm_value(args.flow_rate, args.model)

        # Apply the PWM signal to the pump
        pwm.ChangeDutyCycle(pwm_value)

        # Print details for monitoring
        print(f"Model: {args.model}, Desired Flow Rate: {args.flow_rate} mL/min, PWM Duty Cycle: {pwm_value:.2f}%")

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm.stop()  # Stop the PWM output
    GPIO.cleanup()  # Clean up GPIO settings