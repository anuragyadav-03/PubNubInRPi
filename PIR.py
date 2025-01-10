import RPi.GPIO as GPIO
import time

PIR_Pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_Pin, GPIO.IN)

try:
    print("PIR Sensor initialized. Press Ctrl+C to exit.")
    time.sleep(2)  # Allow the sensor to stabilize

    while True:
        if GPIO.input(PIR_Pin):
            print("Motion Detected!")
        else:
            print("No Motion")
        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()  # Clean up GPIO settings
