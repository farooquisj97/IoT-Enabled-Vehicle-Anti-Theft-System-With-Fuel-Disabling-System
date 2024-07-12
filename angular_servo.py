from gpiozero import AngularServo
from time import sleep

# Constants for the module
SERVO_PIN = 18  # Default GPIO pin for the servo
DEFAULT_FREQ = 50  # Default frequency for servo control (50 Hz)

# Initialize the Angular Servo
def initialize_servo(pin=SERVO_PIN):
    """Initialize Angular Servo on the given pin."""
    servo = AngularServo(
        pin,
        min_angle=0,
        max_angle=180,
        min_pulse_width=0.5 / 1000,  # 500 microseconds
        max_pulse_width=2.5 / 1000,  # 2500 microseconds
    )
    return servo

# Set the angle for the servo
def set_servo_angle(servo, angle):
    """Set the servo to a specific angle."""
    servo.angle = angle
    print(angle)
    sleep(1)  # Allow time for the servo to move

# Move the servo through a range of angles
def move_servo(servo):
    """Move the servo from 0 to 180 degrees and back."""
    for angle in range(0, 181, 5):  # Increment by 45 degrees
        set_servo_angle(servo, angle)
    
    for angle in range(180, -1, -5):  # Decrement by 45 degrees
        set_servo_angle(servo, angle)

# Main function
def main(state):
    """Control the Angular Servo."""
    servo = initialize_servo()  # Initialize the servo
    
    if state:
        set_servo_angle(servo, 0)
    else:
        set_servo_angle(servo, 90)
    
    
    
if __name__ == "__main__":
    while True:
        main(True)  # Execute the main function if run as a standalone script
        main(False)
