import requests
import paho.mqtt.publish as publish
import json
from geopy.geocoders import Nominatim

def get_location_name(latitude, longitude):
    """Get location name from coordinates."""
    geolocator = Nominatim(user_agent="location_receiver")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address if location else "Unknown Location"

def get_ip_location():
    """Get Raspberry Pi's location based on IP geolocation."""
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        coordinates = data['loc'].split(',')
        return float(coordinates[0]), float(coordinates[1])
    except Exception as e:
        print("Failed to retrieve IP location:", str(e))
        return None

def send_ip_location_to_mqtt(broker_address, port, topic, username):
    """Send Raspberry Pi's location based on IP geolocation to MQTT Broker."""
    latitude, longitude = get_ip_location()
    if latitude and longitude:
        location_name = get_location_name(latitude, longitude)
        message = {
            "latitude": latitude,
            "longitude": longitude,
            "Area": location_name
        }
        try:
            publish.single(topic, json.dumps(message), qos=1, hostname=broker_address, port=port, auth={'username': username})
            print("Location sent successfully")
            print(message)
        except Exception as e:
            print("Failed to send location:", str(e))
    else:
        print("Failed to obtain Raspberry Pi's coordinates.")

def main():
    # MQTT Broker Details
    broker_address = "demo.thingsboard.io"
    port = 1883
    topic = "v1/devices/me/telemetry"
    username = "Tracker1id0987654321"  # Your username or device ID
    send_ip_location_to_mqtt(broker_address, port, topic, username)

if __name__ == "__main__":
    main()
