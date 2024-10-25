import RPi.GPIO as GPIO
import time

# Pin setup
pump_control_pin = 18  # GPIO 18 for PWM output
desired_flow_rate = 100  # Desired flow rate in mL/min (adjust as needed)

# Model type (0 for KP, 1 for KT)
model_type = 0  # Set to 0 for KP model, 1 for KT model

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_control_pin, GPIO.OUT)

# Initialize PWM on GPIO 18 at 1000 Hz
pwm = GPIO.PWM(pump_control_pin, 1000)  # 1000 Hz frequency
pwm.start(0)  # Start PWM with 0% duty cycle (pump off)

def calculate_pwm_value(flow_rate, model_type):
    """
    Function to calculate PWM duty cycle based on the desired flow rate.
    Handles both KP and KT models:
    - KP: 0.5V = 0 mL/min, 5V = 150 mL/min
    - KT: 0.5V = 0 mL/min, 5V = 130 mL/min
    """
    if model_type == 0:  # KP model
        slope = 33.33  # Flow rate per volt for KP model
    else:  # KT model
        slope = 28.89  # Flow rate per volt for KT model

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

try:
    while True:
        # Calculate the PWM value for the desired flow rate and model type
        pwm_value = calculate_pwm_value(desired_flow_rate, model_type)

        # Apply the PWM signal to the pump
        pwm.ChangeDutyCycle(pwm_value)

        # Print details for monitoring
        if model_type == 0:
            model_name = "KP"
        else:
            model_name = "KT"
        print(f"Model: {model_name}, Desired Flow Rate: {desired_flow_rate} mL/min, PWM Duty Cycle: {pwm_value:.2f}%")

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm.stop()  # Stop the PWM output
    GPIO.cleanup()  # Clean up GPIO settings