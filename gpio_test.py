import RPi.GPIO as GPIO
import time

# Pin configuration
led_pin = 18  # GPIO pin for the LED
button_pin = 23  # GPIO pin for the button

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        # Read the button state
        button_state = GPIO.input(button_pin)

        if button_state == GPIO.LOW:
            # Button is pressed, turn on the LED
            GPIO.output(led_pin, GPIO.HIGH)
            print("Button pressed, LED on")
        else:
            # Button is not pressed, turn off the LED
            GPIO.output(led_pin, GPIO.LOW)
            print("Button not pressed, LED off")

        # Wait for a short period to debounce the button
        time.sleep(0.1)

except KeyboardInterrupt:
    pass  # Exit cleanly on Ctrl+C

finally:
    GPIO.cleanup()  # Clean up GPIO settings