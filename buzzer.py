import RPi.GPIO as GPIO
import time

Buzzer_Pin = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Buzzer_Pin, GPIO.OUT)

try:
    while True:
        # Turn on the buzzer
        GPIO.output(Buzzer_Pin, True)
        time.sleep(1)  # Buzzer sounds for 1 second

        # Turn off the buzzer
        GPIO.output(Buzzer_Pin, False)
        time.sleep(1)  # Pause for 1 second before the next beep

except KeyboardInterrupt:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
