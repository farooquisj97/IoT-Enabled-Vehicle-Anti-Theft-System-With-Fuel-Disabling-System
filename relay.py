import RPi.GPIO as GPIO
import time

def initialize_relay(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

def turn_relay_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    print("Relay on, starter disabled")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def turn_relay_off(pin):
    GPIO.output(pin, GPIO.LOW)
    print("Relay off, starter enabled")

def cleanup():
    GPIO.cleanup()

def main(state):
    # Replace RELAY_PIN with the actual GPIO pin number
    RELAY_PIN = 15
    initialize_relay(RELAY_PIN)
    if state:
        turn_relay_on(RELAY_PIN)
    else:
        turn_relay_off(RELAY_PIN)
                

if __name__ == "__main__":
    main()
                                        
