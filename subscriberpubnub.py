import time
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback


# PubNub Configuration
config = PNConfiguration()
config.subscribe_key = 'sub-c-f3d64305-2b22-4b82-b72d-74fb6093fe74'  # Replace with your actual subscribe key
config.publish_key = 'pub-c-fa518d5d-8837-4617-b351-101b4eca59e0'  # Replace with your actual publish key
config.user_id = 'raspi'  # Can be any string identifying your user
config.auth_key = 'p0F2AkF0GmeBBtpDdHRsGDxDcmVzpURjaGFuoWRSU1BZGM9DZ3JwoWltaW5kYmxhemUYz0NzcGOgQ3VzcqBEdXVpZKFlcmFzcGkYz0NwYXSlRGNoYW6gQ2dycKBDc3BjoEN1c3KgRHV1aWSgRG1ldGGgQ3NpZ1ggjGkm-S0K-vHN7zVBUSRdFN0UOfngJpH0awFfL0gLiRM='

pubnub = PubNub(config)


class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        print(f"Status: {status.category.name}")

    def message(self, pubnub, message):
        try:
            # Print the received message
            print(f"Message received: {message.message}")
            # If you want to process specific data, you can do so here:
            if "motion" in message.message:
                print(f"Motion Status: {message.message['motion']}")
        except Exception as e:
            print(f"Error processing message: {e}")


if __name__ == '__main__':
    try:
        # Add listener to the PubNub instance
        pubnub.add_listener(MyListener())

        # Subscribe to the channel
        pubnub.subscribe().channels("RSPY").execute()  # Ensure to use the same channel as your publisher

        # Keep the subscriber running indefinitely
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Exiting program.")
