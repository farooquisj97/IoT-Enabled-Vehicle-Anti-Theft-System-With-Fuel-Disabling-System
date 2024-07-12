import RPi.GPIO as GPIO
import time

# Set pin 11 as output
servo_pin = 32

def initialize_servo(pin):
    """Initialize servo pin."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

def set_angle(angle, pwm):
    """Set servo angle."""
    duty = angle / 18 + 2  # Convert angle to duty cycle
    pwm.ChangeDutyCycle(duty)
    #print(angle)
    time.sleep(0.005)  # Wait for the servo to reach the position
    
    
    
def move_servo(pwm):
    """Move servo from 0 to 180 degrees and back."""
    try:
        pwm.start(0)  # Start PWM with 0% duty cycle (servo at 0 degrees)
        # Move servo from 0 to 90 degrees
        for angle in range(0, 91, 1):
            set_angle(angle, pwm)
            
        # Move servo from 90 to 0 degrees
        for angle in range(90, -1, -1):
            set_angle(angle, pwm)

    except KeyboardInterrupt:
        # Cleanup GPIO
        pwm.stop()
        GPIO.cleanup()
        

def injection_disable(pwm):
    pwm.start(0)
    for angle in range(0, 91, 1):
        set_angle(angle, pwm)


def injection_enable(pwm):
    pwm.start(90)
    for angle in range(90, -1, -1):
        set_angle(angle, pwm)


def main(state):
    initialize_servo(servo_pin)
    # Set PWM instance
    pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz (20 ms PWM period)
    
    if state:
        injection_disable(pwm)
        print("Fuel injection disabled")
    else:
        injection_enable(pwm)
        print("Fuel injection enabled")
        
        
if __name__ == "__main__":
    print("Servo is enabled")
    main(True)
