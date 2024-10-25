import RPi.GPIO as GPIO
import time

# Pin setup
pump_control_pin = 18  # GPIO 18 is used for PWM output
desired_flow_rate = 100  # Desired flow rate in mL/min (adjust as needed)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pump_control_pin, GPIO.OUT)

# Initialize PWM on GPIO 18 at 1000 Hz
pwm = GPIO.PWM(pump_control_pin, 1000)  # 1000 Hz frequency
pwm.start(0)  # Start PWM with 0% duty cycle (pump off)

def calculate_pwm_value(flow_rate):
    """
    Function to calculate PWM duty cycle based on desired flow rate.
    Assumes 0.5V = 0 mL/min and 5V = 150 mL/min (KP model).
    """
    # Calculate control voltage for KP model (150 mL/min at 5V)
    control_voltage = (flow_rate / 33.33) + 0.5  # 33.33 mL/min per volt

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
        # Calculate the PWM value for the desired flow rate
        pwm_value = calculate_pwm_value(desired_flow_rate)

        # Apply the PWM signal to the pump
        pwm.ChangeDutyCycle(pwm_value)

        # Print details for monitoring
        print(f"Desired Flow Rate: {desired_flow_rate} mL/min, PWM Duty Cycle: {pwm_value:.2f}%")

        # Wait for 1 second before updating
        time.sleep(1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    pwm.stop()  # Stop the PWM output
    GPIO.cleanup()  # Clean up GPIO settings