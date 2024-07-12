import gpsd
import paho.mqtt.publish as publish
import json
from geopy.geocoders import Nominatim


def get_location_name(latitude, longitude):
    """Get location name from coordinates."""
    geolocator = Nominatim(user_agent="location_receiver")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.address if location else "Unknown Location"

def get_gps_location():
    """Get Raspberry Pi's location based on GPS module."""
    try:
        gpsd.connect()
        packet = gpsd.get_current()
        if packet.mode >= 2:
            return packet.lat, packet.lon
        else:
            print("GPS signal not available.")
            return None
    except Exception as e:
        print("Failed to retrieve GPS location:", str(e))

def send_location_to_mqtt(broker_address, port, topic, username):
    """Send Raspberry Pi's location to MQTT Broker."""
    raspberry_pi_coords = get_gps_location()
    if raspberry_pi_coords:
        location_name = get_location_name(raspberry_pi_coords[0], raspberry_pi_coords[1])
        message = {
            "latitude": raspberry_pi_coords[0],
            "longitude": raspberry_pi_coords[1],
            "Area": location_name
        }
        try:
            publish.single(topic, json.dumps(message), qos=1, hostname=broker_address, port=port, auth={'username': username})
            print("Location sent successfully")
            print(message)
        except Exception as e:
            print("Failed to send location:", str(e))
    else:
        print("Failed to obtain Raspberry Pi's coordinates from GPS module.")


def main():
    broker_address = "demo.thingsboard.io"
    port = 1883
    topic = "v1/devices/me/telemetry"
    username = "Tracker1id0987654321"  # Your username or device ID
    send_location_to_mqtt(broker_address, port, topic, username)

if __name__ == "__main__":
    print("GPS is enabled")
    main()
