import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'Tracker1id0987654321'

# We assume that all GPIOs are LOW
gpio_state = {
                7: False, 11: False, 12: False, 13: False, 15: False, 16: False, 
                18: False, 22: False, 29: False, 31: False, 32: False, 33: False, 
                35: False, 36: False, 37: False, 38: False, 40: False
             }

def initialize_gpio_pins(gpio_state):
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

def get_gpio_status():
    """Encode GPIOs state to JSON."""
    return json.dumps(gpio_state)

def set_gpio_status(pin, status):
    """Update GPIO status."""
    GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)
    gpio_state[pin] = status

def main():
    initialize_gpio_pins(gpio_state)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    # Register connect callback
    client.on_connect = on_connect
    # Registered publish message callback
    client.on_message = on_message
    # Set access token
    client.username_pw_set(ACCESS_TOKEN)
    # Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
    client.connect(THINGSBOARD_HOST, 1883, 60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
