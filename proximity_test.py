import smbus
import time

# Define I2C address of the sensor
SENSOR_ADDR = 0x39  # Default address for APDS-9930

# Register addresses
REG_ENABLE = 0x80
REG_ATIME = 0x81
REG_CONTROL = 0x8F
REG_ID = 0x92
REG_PDATAL = 0x8C
REG_PDATAH = 0x8D
REG_STATUS = 0x93

# Commands
CMD_WORD = 0xA0
CMD_CLEAR = 0xE5

# Create an instance of the smbus library
bus = smbus.SMBus(1)  # Use /dev/i2c-1 for Raspberry Pi 2/3

# Function to initialize the sensor
def init_sensor():
    # Enable the sensor
    bus.write_byte_data(SENSOR_ADDR, REG_ENABLE | CMD_WORD, 0x03)  # Enable proximity and ambient light sensing
    bus.write_byte_data(SENSOR_ADDR, REG_ATIME | CMD_WORD, 0xDB)   # Set ATIME (Integration Time) - Adjust according to your requirement
    bus.write_byte_data(SENSOR_ADDR, REG_CONTROL | CMD_WORD, 0x03) # Set CONTROL register (Proximity gain = 1x, ALS gain = 1x)

# Function to read proximity data
def read_proximity():
    data = bus.read_word_data(SENSOR_ADDR, REG_PDATAL | CMD_WORD)
    proximity = ((data & 0xFF) << 8) | ((data >> 8) & 0xFF)
    return proximity

# Function to read ambient light data
def read_ambient_light():
    data = bus.read_word_data(SENSOR_ADDR, REG_PDATAL | CMD_WORD)
    ambient_light = ((data & 0xFF) << 8) | ((data >> 8) & 0xFF)
    return ambient_light

# Function to check if the sensor is present
def is_sensor_present():
    try:
        sensor_id = bus.read_byte_data(SENSOR_ADDR, REG_ID | CMD_WORD)
        print("Sensor ID:", hex(sensor_id))
        return sensor_id == 0xAB
    except Exception as e:
        print("Error reading sensor ID:", e)
        return False

# Initialize the sensor
'''
if is_sensor_present(): # if is_sensor_present() == True:
    print("Sensor found!")
    init_sensor()
else:
    print("Sensor not found!")
    exit()
'''

init_sensor()
try:
	
    while True:
		
        # Read proximity data
        proximity_data = read_proximity()
        
        # Read ambient light data
        ambient_light_data = read_ambient_light()
        
        # Print the data
        print("Proximity:", proximity_data)
        print("Ambient Light:", ambient_light_data)
        
        # Wait before reading again
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program terminated by user")
