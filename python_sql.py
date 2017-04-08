import sqlite3          # For SQLite library and capability
import datetime         # Import 'datatime' library to record time stamps
import RPi.GPIO as GPIO # Import GPIO Library
import time             # Import 'time' library.  Allows us to use 'sleep'
import spidev           # Interface used for MCP3008 ADC

# DEFINE TESTING VARIABLES (these change while testing)
tries = 20  # Number of measurements to take
v_ref = 2.5     # Max voltage value of incoming signal
c_resistor = 1200   # Value of resistor used to calculate current

# Define variables
delay = 0.25    # Delay between measurements (seconds)
analog_channel = 0  # Channel of MCP3008 ADC to read from
curr_scale = 1000 # Current scale factor to convert A to mA
#v_ref = ??    # WILL BE CALIBRATED AND CONSTANT FOR DEMO
#c_resistor = ??   # WILL BE CALIBRATED AND CONSTANT FOR DEMO

# Create SPI
spi = spidev.SpiDev()
spi.open(0,0)

# Function to read from ADC
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

conn = sqlite3.connect('test')

c = conn.cursor()

for i in range(0,tries):
    analog_value = readadc(analog_channel)  # Read channel
    dateTime = datetime.datetime.now()      # Get timestamp
    voltage = (analog_value*v_ref)/(2**10)       # Convert to voltage
    current = voltage/c_resistor                  # Calculate current
    power = voltage*current                 # Calculate power
    print ("---------------------------------------")   # Display
    print("Analog Value: %d" % analog_value)
    print("Voltage Value: %f" % voltage)
    print("Current Value: %f" % current)
    print("Power Value: %f" % power)
    c.execute("INSERT INTO test VALUES (?,?,?,?,?)", (i+1,voltage,current,power,dateTime))  # Update database
    time.sleep(delay)

conn.commit()
conn.close()
