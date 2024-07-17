import threading
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import input_trigger as trig
import json
import gps
import buzzer
import angular_servo
import relay
import time

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = "Your username or device ID"

TRIG = 7
USER = 11

GPS = 31
BUZZER = 33
SERVO = 35
RELAY = 37

''' pin connection (board mode)
starter==> 7
user   ==> 11
gps    ==> rx-tx
buzzer ==> 13 ie GPIO 27
servo  ==> 12 ie GPIO 18
relay  ==> 15 ie GPIO 22
'''

# Boolean storing state of devices
peripherals = { 
		gps: False, 
		buzzer: False, 
		angular_servo: False, 
		relay: False
             }

# Pins accessed by Thingsboard server via mqtt
gpio_state = {
                GPS: False, BUZZER: False, SERVO: False, RELAY: False
             }

def initialize_gpio_pins():
    """Initialize GPIO pins."""
    GPIO.setmode(GPIO.BOARD)
    for pin in gpio_state:
        GPIO.setup(pin, GPIO.OUT)


def on_connect(client, userdata, rc, *extra_params):
    """Callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    # Subscribing to receive RPC requests
    client.subscribe('v1/devices/me/rpc/request/+')
    # Sending current GPIO status
    client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    print('Topic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
    # Decode JSON request
    data = json.loads(msg.payload)
    # Check request method
    if data['method'] == 'getGpioStatus':
        # Reply with GPIO status
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
    elif data['method'] == 'setGpioStatus':
        # Update GPIO status and reply
        set_gpio_status(data['params']['pin'], data['params']['enabled'])
        client.publish(msg.topic.replace('request', 'response'), get_gpio_status(), 1)
        client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


def on_action(peripherals):
    angular_servo.main(peripherals[angular_servo])
    relay.main(peripherals[relay]) 
    
    
def get_gpio_status():
    """Encode GPIOs state to JSON."""
    return json.dumps(gpio_state)


def set_gpio_status(pin, status):
    """Update GPIO status."""
    GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    gpio_state[pin] = status
    peripherals[gps] = gpio_state[GPS]
    peripherals[buzzer] = gpio_state[BUZZER]
    peripherals[angular_servo] = gpio_state[SERVO]
    peripherals[relay] = gpio_state[RELAY]
            
    on_action(peripherals)
        

def mqtt_client():
    initialize_gpio_pins()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # Register connect callback
    client.on_connect = on_connect
    # Registered publish message callback
    client.on_message = on_message
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)
    client.loop_forever()


def looped_controls():
    while True:
        if peripherals[gps]:
            gps.main()
        if peripherals[buzzer]:
            buzzer.main()
        time.sleep(0.3)
    

def main():
    trig.read_input_pins(TRIG, USER)


if __name__ == "__main__":
    try:
        mqtt_thread = threading.Thread(target=mqtt_client)
        mqtt_thread.daemon = True  # Ensures it closes when main program ends
        ctrl_thread = threading.Thread(target=looped_controls)
        ctrl_thread.daemon = True
        mqtt_thread.start()
        ctrl_thread.start()
        main()        
    except KeyboardInterrupt:
        GPIO.cleanup()

