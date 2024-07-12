import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import gps
import time
import json
import send2telegram

TRIG = 7
USER = 11

def read_input_pins(pin1, pin2):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin1, GPIO.IN)
    GPIO.setup(pin2, GPIO.IN)

    previous_state1 = GPIO.input(pin1)
    previous_state2 = GPIO.input(pin2)
    
    while True:
        current_state1 = GPIO.input(pin1)
        current_state2 = GPIO.input(pin2)
        
        if current_state1 != previous_state1 or current_state2 != previous_state2:  
            main(current_state1, current_state2)  
            previous_state1 = current_state1
            previous_state2 = current_state2
            
        time.sleep(0.1)

def main(state1, state2):
    print(f"User: {'Verified' if state2 else 'Unknown'}", end='\t')
    print(f"Starter: {'ON' if state1 else 'OFF'}")

    dashboard = "https://demo.thingsboard.io/dashboards/363e3810-f265-11ee-81e8-7942c9f23c0f"
    if state1 and not state2:
        try:
            coord = gps.get_gps_location()
            link = f"https://www.google.com/maps?q={coords[0]},{coords[1]}"
            msg = f"##ALERT## \nUNKOWN user started your vehicle. You can check the last location here: \n {link} \nGo to the vehicle dashboard: \n {dashboard}"
        except:
            print("Could not retrive location")
            msg = f"##ALERT## \nUNKOWN user started your vehicle. \nGo to the vehicle dashboard: \n {dashboard}"
        finally:
            send2telegram.main(msg)

def get_msg():
    coords = last_location()
    return msg

def mqtt(state1, state2):
    # MQTT Configuration
    THINGSBOARD_HOST = 'demo.thingsboard.io'
    ACCESS_TOKEN = 'Tracker1id0987654321'  # Replace with your access token
    
    # Check conditions for alert
    if state1 and not state2:
        print("******** Alert notified! ********")
        # Connect to MQTT broker
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.username_pw_set(ACCESS_TOKEN)
        client.connect(THINGSBOARD_HOST, 1883, 60)
        msg = get_msg()
        # Publish alert message
        client.publish("v1/devices/me/telemetry", msg, 1)
        client.disconnect()
        
    
    print("Input states changed:")
    print(f"Starter: {'ON' if state1 else 'OFF'}")
    print(f"User: {'Verified' if state2 else 'Unknown'}")

if __name__ == "__main__":
    read_input_pins(TRIG, USER)
