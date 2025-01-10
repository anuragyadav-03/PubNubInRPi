import RPi.GPIO as GPIO
import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# GPIO Pin Setup
PIR_Pin = 24
LED_Pin = 18

# PubNub Configuration
myChannel = "RSPY"
sensorsList = ["buzzer"]
data = {}

config = PNConfiguration()
config.subscribe_key = 'sub-c-f3d64305-2b22-4b82-b72d-74fb6093fe74'  # Replace with your actual subscribe key
config.publish_key = 'pub-c-fa518d5d-8837-4617-b351-101b4eca59e0'  # Replace with your actual publish key
config.user_id = 'raspi'
config.auth_key = 'p0F2AkF0GmeBBtpDdHRsGDxDcmVzpURjaGFuoWRSU1BZGM9DZ3JwoWltaW5kYmxhemUYz0NzcGOgQ3VzcqBEdXVpZKFlcmFzcGkYz0NwYXSlRGNoYW6gQ2dycKBDc3BjoEN1c3KgRHV1aWSgRG1ldGGgQ3NpZ1ggjGkm-S0K-vHN7zVBUSRdFN0UOfngJpH0awFfL0gLiRM='

pubnub = PubNub(config)

# GPIO setup (Move this code outside the thread to ensure it runs before the thread starts)
GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)  # Set the pin numbering mode to BCM

# Debugging print to ensure setmode is called
print("GPIO Mode set to BCM")

GPIO.setup(PIR_Pin, GPIO.IN)
GPIO.setup(LED_Pin, GPIO.OUT)

# LED Blink function
def blink_led(repeat):
    for i in range(repeat):
        GPIO.output(LED_Pin, True)
        time.sleep(0.5)
        GPIO.output(LED_Pin, False)
        time.sleep(0.5)

# Motion Detection function
def motionDetection():
    global data
    testing = 10
    data["Led_On"] = False
    print("Sensors Started")
    trigger = False
    while True:
        # print("Checking PIR sensor...")
        # publish(myChannel, "Testing")
        # if GPIO.input(PIR_Pin): 
        if testing > 0: 
            print("Motion Detected")
            blink_led(4)
            trigger = True
            message = {"motion": "Yes"}
            publish(myChannel, message)
            time.sleep(1)
        elif trigger:  # If trigger is True and no motion is detected, send "No"
            print("No Motion")
            message = {"motion": "No"}
            publish(myChannel, message)
            trigger = False  # Reset trigger after sending "No"
            time.sleep(1)

        if data["Led_On"]:
            blink_led(2)

        time.sleep(0.1)  # Short delay to avoid excessive polling of the GPIO

# Publish function to send messages to PubNub
def publish(channel, msg):
    # Print the message before sending it to PubNub
    print(f"Publishing to channel {channel}: {msg}")
    pubnub.publish().channel(channel).message(msg).sync()

# Listener for PubNub
class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        category = status.category
        if category == "PNConnectedCategory":
            print("Device connected successfully!")
        elif category == "PNReconnectedCategory":
            print("Device reconnected!")
        elif category == "PNDisconnectedCategory":
            print("Device disconnected!")
        elif category == "PNTimeoutCategory":
            print("Timeout occurred while trying to connect!")
        elif category == "PNNetworkDownCategory":
            print("Network is down!")
        elif category == "PNNetworkUpCategory":
            print("Network is back up!")
        elif category == "PNUnknownCategory":
            print("Unknown category!")
        else:
            print(f"Unhandled status category: {category}")

    def message(self, pubnub, message):
        try:
            print(message.message, ": ", type(message.message))
            msg = message.message
            print("Received JSON:", msg)
            key = list(msg.keys())
            if key[0] == "event":
                self.handleEvent(msg)
        except Exception as e:
            print(f"Error processing message: {e}")

    def handleEvent(self, msg):
        global data
        eventData = msg["event"]
        key = list(eventData.keys())
        if key[0] in sensorsList:
            if eventData[key[0]] is True:
                data["Led_On"] = True
            elif eventData[key[0]] is False:
                data["Led_On"] = False

# Main function to start listening for PubNub events and perform motion detection
if __name__ == '__main__':
    try:
        # Run the motion detection function directly in the main thread
        motionDetection()

        # Start the PubNub listener
        pubnub.add_listener(MyListener())
        pubnub.subscribe().channels(myChannel).execute()

    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        GPIO.cleanup()  # Clean up GPIO to ensure the pins are released
