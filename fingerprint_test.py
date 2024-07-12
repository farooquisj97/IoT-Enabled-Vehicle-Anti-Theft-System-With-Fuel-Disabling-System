import RPi.GPIO as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
import csv
import datetime

GPIO.setwarnings(False)
# GPIO pin numbers
tx_pin = 14
rx_pin = 15

# Function to initialize fingerprint sensor
def initialize_sensor():
    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(tx_pin, GPIO.OUT)
    GPIO.setup(rx_pin, GPIO.IN)
    print("Initializing fingerprint sensor")
    try:
        # port /dev/tty7 coz no permissions required  (ls -al /dev/tty*)
        f = PyFingerprint('/dev/tty7', 9600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')
        return f
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        GPIO.cleanup()
        exit(1)

# Function to enroll student fingerprint
def enroll_student(f):
    print("Place your finger on the sensor to enroll...")
    while True:
        if f.readImage() == True:
            f.convertImage(0x01)
            result = f.searchTemplate()
            positionNumber = result[0]
            if positionNumber >= 0:
                print("Fingerprint already enrolled. Try again.")
                continue
            else:
                print("Remove your finger...")
                time.sleep(2)
                print("Place your finger again...")
                f.convertImage(0x02)
                if f.compareCharacteristics() == 0:
                    print("Fingerprints do not match. Try again.")
                    continue
                f.createTemplate()
                positionNumber = f.storeTemplate()
                print("Fingerprint enrolled successfully!")
                return positionNumber
        time.sleep(1)

# Function to detect fingerprint for attendance
def detect_fingerprint(f):
    print("Place your finger on the sensor to detect...")
    if f.readImage() == True:
        f.convertImage(0x01)
        result = f.searchTemplate()
        positionNumber = result[0]
        if positionNumber >= 0:
            return True, positionNumber
        else:
            return False, None
    else:
        print("Failed to read fingerprint image.")
        return False, None

# Function to update attendance in CSV file
def update_attendance_csv(student_name, status):
    filename = "attendance.csv"
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([student_name, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), status])
    print(f"Attendance recorded for {student_name}.")

# Function to print acknowledgment message
def print_acknowledgment(student_name):
    print(f"Attendance recorded for {student_name} on {datetime.datetime.now()}")


# Main code
try:
    # Initialize fingerprint sensor
    fingerprint_sensor = initialize_sensor()

    # Main loop
    while True:
        option = input("Enter 'r' to register a new student, 'd' to take attendance, or 'q' to quit: ")
        
        if option == 'r':
            student_name = input("Enter student's name: ")
            position_number = enroll_student(fingerprint_sensor)
            # Store enrolled fingerprint with student's name and position number
            # (You can store this information in a CSV file or database)
        
        elif option == 'd':
            success, position = detect_fingerprint(fingerprint_sensor)
            if success:
                student_name = "Unknown"
                # Retrieve student's name associated with the detected fingerprint position number
                # (You can retrieve this information from a CSV file or database)
                if student_name:
                    update_attendance_csv(student_name, "Present")
                    print_acknowledgment(student_name)
                else:
                    print("Student information not found.")
            else:
                print("No fingerprint detected.")
        
        elif option == 'q':
            break
        
        else:
            print("Invalid option. Please try again.")

except KeyboardInterrupt:
    print("Attendance system stopped by user.")

finally:
    # Cleanup GPIO
    GPIO.cleanup()
