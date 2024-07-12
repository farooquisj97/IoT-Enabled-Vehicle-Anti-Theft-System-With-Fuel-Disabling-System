from datetime import datetime
import csv
import time
import RPi.GPIO as GPIO
from adafruit_fingerprint import Adafruit_Fingerprint

# Define GPIO pins for software serial communication
TX_PIN = 14  # GPIO pin for transmitting data (connect to fingerprint sensor RX)
RX_PIN = 15  # GPIO pin for receiving data (connect to fingerprint sensor TX)

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TX_PIN, GPIO.OUT)
GPIO.setup(RX_PIN, GPIO.IN)


# Initialize the fingerprint sensor with software serial
fingerprint_sensor = Adafruit_Fingerprint(TX_PIN, RX_PIN)

# Set the fingerprint sensor password
fingerprint_password = bytearray([0, 0, 0, 0])
fingerprint_sensor.password = fingerprint_password

# Define UART baudrate
BAUDRATE = 57600
fingerprint_sensor.baudrate = BAUDRATE


# Define CSV file path
CSV_FILE = "fingerprint_data.csv"

# Function to register a fingerprint with a name
def register_fingerprint(name):
    try:
        # Get fingerprint image
        if fingerprint_sensor.get_image() == fingerprint_sensor.OK:
            print("Image taken successfully.")
            if fingerprint_sensor.image_2_tz() == fingerprint_sensor.OK:
                print("Image converted successfully.")
                if fingerprint_sensor.create_model() == fingerprint_sensor.OK:
                    print("Fingerprint model created.")
                    if fingerprint_sensor.store_model(len(name), 1) == fingerprint_sensor.OK:
                        print("Fingerprint stored successfully.")
                        # Append fingerprint data to CSV file along with name and timestamp
                        append_to_csv(name)
                    else:
                        print("Failed to store fingerprint.")
                else:
                    print("Failed to create fingerprint model.")
            else:
                print("Failed to convert image.")
        else:
            print("Failed to take image.")
    except Exception as e:
        print("Error registering fingerprint:", e)

# Function to append fingerprint data to CSV file along with name and timestamp
def append_to_csv(name):
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        # Append data to CSV file
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, timestamp])

        print("Data appended to CSV successfully.")
    except Exception as e:
        print("Error appending data to CSV:", e)

# Function to read fingerprint and get the date and time
def read_fingerprint():
    try:
        # Assuming fingerprint search is successful and returns finger_id and confidence
        finger_id, confidence = fingerprint_sensor.finger_search()

        if finger_id is not None:
            print("Fingerprint found with ID:", finger_id)
            # Get current timestamp
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            print("Timestamp:", timestamp)
            # Append fingerprint ID and timestamp to CSV file
            append_to_csv(f"Fingerprint {finger_id}")
        else:
            print("Fingerprint not found.")
    except Exception as e:
        print("Error reading fingerprint:", e)

# Main function
def main():
    print("Starting fingerprint process")
    
    try:     
        print("Initialising registering process")
        name = input("Enter name: ")
        
        # Register a fingerprint with a name
        register_fingerprint(name)

        # Read a fingerprint and get the date and time
        read_fingerprint()
        
        print("Process complete")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
    finally:
        # Clean up GPIO
        GPIO.cleanup()

if __name__ == "__main__":
    main()
