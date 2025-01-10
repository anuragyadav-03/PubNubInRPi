from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)

alive = 0
data = {}
PIR_Pin = 24
LED_Pin = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_Pin, GPIO.IN)
GPIO.setup(LED_Pin, GPIO.OUT)

def blink_led(repeat):
    for i in range(repeat):
        GPIO.output(LED_Pin, True)
        time.sleep(0.5)
        GPIO.output(LED_Pin, False)
        time.sleep(0.5)

def motionDetection():
    global data
    while True:
        if GPIO.input(PIR_Pin):  
            print("Motion Detected")
            blink_led(4) 
            data["motion"] = 1
        else:
            data["motion"] = 0
            print("No Motion")  
        time.sleep(1)

@app.route("/")
def hello():
    return render_template("index.html")
    # return "Hii"

@app.route('/keep_alive', methods=['GET'])
def keep_alive():
    global alive, data
    alive += 1
    data['keep_alive'] = str(alive)
    data['Server'] = str("Raspi Server")
    return jsonify(data)
    
@app.route("/status", methods=['POST'])
def event():
    global data
    request_data = request.get_json() 
    led_state = request_data.get("state")

    if led_state == 1:
        print("LED: ON")
        data["Led_On"] = True
    else:
        print("LED: OFF")
        data["Led_On"] = False

    return "OK"

if __name__ == '__main__':
    # Start the motion detection in a separate thread
    motion_thread = threading.Thread(target=motionDetection)
    motion_thread.daemon = True  # Ensure thread exits when main program exits
    motion_thread.start()
    
    app.run(host="0.0.0.0", port=7506)
