import RPi.GPIO as GPIO
import time

# Setup GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 23  # Define the GPIO pin number

# Setup the pin as output
GPIO.setup(PIN, GPIO.OUT)

# Function to toggle the pin state
def toggle_pin(pin, duration=1):
    GPIO.output(pin, GPIO.HIGH)  # Turn on
    time.sleep(duration)
    GPIO.output(pin, GPIO.LOW)   # Turn off
    time.sleep(duration)

if __name__ == '__main__':
    try:
        while True:
            toggle_pin(PIN, 1)  # Toggle every 1 second
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Reset GPIO settings
