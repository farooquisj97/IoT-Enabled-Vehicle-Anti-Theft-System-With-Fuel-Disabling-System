import RPi.GPIO as GPIO
import time


def initialize_buzzer(pin):
    """Initialize buzzer pin."""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

def play_sound(frequency, pwm):
    """Play sound with variable frequency."""
    pwm.ChangeFrequency(frequency)
    pwm.start(50)  # Start PWM with 50% duty cycle (0-100)
    time.sleep(0.5)  # Play sound for 0.5 seconds
    pwm.stop()  # Stop PWM

def buzz(pwm):
    """Generate buzzing sound."""
    for i in range(30, 100, 30):
        play_sound(i * 100, pwm)
        print(i * 100)
        time.sleep(0.01)

def main():
    # Set pin 13 as output
    buzzer_pin = 13
    initialize_buzzer(buzzer_pin)
    # Set PWM instance
    pwm = GPIO.PWM(buzzer_pin, 100)  # 100 Hz PWM frequency

    try:
        # Play sound at different frequencies (adjust as needed)
        #buzz(pwm)
        play_sound(800, pwm)
        time.sleep(0.01)
    except KeyboardInterrupt:
        # Cleanup GPIO
        pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    print("Buzzer is enabled")
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
