import socket
import threading
import time
import RPi.GPIO as GPIO # Import GPIO Library
import sqlite3
import datetime
import spidev
import sys

# 1. Needs to know if a client is connected
# 2. How to SEND data? - remember it's sent as bytes
# 3. Remove the b'....' from the incoming message

# http://studyswift.blogspot.com/2016/03/communication-between-ios-device-client.html

pin1 = 22
pin2 = 32
pin3 = 36
pin4 = 38

GPIO.setmode(GPIO.BOARD) ## Use BOARD pin numbering - Basic sequence
GPIO.setup(pin1, GPIO.OUT) ## Setup GPIO pin 22 to OUT
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

spi = spidev.SpiDev()
spi.open(0,0)

flag = True     # flag to control thread
globalAvgPower = 0.0

voltage_channel = 4    # Channel to read from on ADC
current_channel = 7    # Channel to read from on ADC

def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def dbThread():
    conn = sqlite3.connect('test')
    cur = conn.cursor()

    tries = 12000  # Number of measurements to take
    v_ref = 3.3     # Max voltage value of incoming signal
    c_ref = 1.465
    c_resistor = 1200   # Value of resistor used to calculate current
    analog_value = 2.345
    delay = 0.008
    count = 0
    avgPower = 0
    sampleRate = 240   # 2 seconds at a 120 Hz
    global globalAvgPower

    # for i in range(0,tries):
    #     # analog_value = readadc(analog_channel)  # Read channel
    #     analog_value += 1.234
    #     dateTime = datetime.datetime.now()      # Get timestamp
    #     voltage = (analog_value*v_ref)/(2**10)       # Convert to voltage
    #     current = voltage/c_resistor                  # Calculate current
    #     power = voltage*current                 # Calculate power
    #     # print ("---------------------------------------")   # Display
    #     # print("Analog Value: %f" % analog_value)
    #     # print("Voltage Value: %f" % voltage)
    #     # print("Current Value: %f" % current)
    #     # print("Power Value: %f" % power)
    #     cur.execute("INSERT INTO test VALUES (?,?,?)", (voltage,power,dateTime))  # Update database
    #     time.sleep(delay)

    #while True:
    for i in range(0,sampleRate):
        #voltage_value = readadc(voltage_channel)  # Read channel
        current_value = readadc(current_channel)
       # voltage = (voltage_value*v_ref)/(2**10)
        voltage = 120
        current = (current_value*v_ref)/(2**10)
        current = (current-c_ref)/0.1       # Convert to voltage
        power = voltage*current                 # Calculate power
        avgPower += power
        print ("---------------------------------------")   # Display
        #print("Voltage Analog Value: %f" % voltage_value)
        print("Current Analog Value: %f" % current_value)
        print("Voltage Value: %f" % voltage)
        print("Current Value: %f" % current)
        print("Power Value: %f" % power)
        if count == sampleRate:
            avgPower /= sampleRate
            globalAvgPower = avgPower
            dateTime = datetime.datetime.now()      # Get timestamp
            #cur.execute("INSERT INTO test VALUES (?,?,?,?)", (voltage,current,power,dateTime))  # Update database
            cur.execute("INSERT INTO avgPower VALUES (?,?)", (avgPower, dateTime))
            print (avgPower)
            avgPower = 0
            count = 0
        count += 1
        time.sleep(delay)
    print('END')
    conn.commit()
    conn.close()
# END dbThread()

def rxThread():
    # Receive/Read message in this thread
    # Outlet Control
    #   -> Code to turn on and off the RPi's pins here
    print (threading.currentThread().getName(), 'Starting')
    time_flag = 1
    global flag

    while flag:
        data = c.recv(1024)
        data = data.decode("utf-8")
        if data == '':
            continue
        #else:
           # print ("\n(rxThread) Recieved: " + data + " from " + addr[0])

        if data == "QUIT":
            # GPIO.output(pin1, 0)
            # GPIO.output(pin2, 0)
            # GPIO.output(pin3, 0)
            # GPIO.output(pin4, 0)
            flag = False        # Close connetion to client (iOS)
            break

        if data == "LED1:on":
            GPIO.output(pin1, 1)
        if data == "LED2:on":
            GPIO.output(pin2, 1) 
        if data == "LED3:on":
            GPIO.output(pin3, 1)
        if data == "LED4:on":
            GPIO.output(pin4, 1)

        if data == "LED1:off":
            GPIO.output(pin1, 0)
        if data == "LED2:off":
            GPIO.output(pin2, 0) 
        if data == "LED3:off":
            GPIO.output(pin3, 0)
        if data == "LED4:off":
            GPIO.output(pin4, 0)
        if (pin1 == 1 or pin2 == 1 or pin3 == 1 or pin4 == 1) and time_flag == 1:
            # start the timer
            start_time = time.time()
            time_flag = 0
        elif pin1 == 0 and pin2 == 0 and pin3 == 0 and pin4 == 0:
            # stop the timer
            end_time = time.time()
            time_flag = 1
            duration = end_time - start_time
            total_duration += duration

    print (threading.currentThread().getName(), 'Exiting')
# END rxThread()

def txThread():
    # Transmit/Send message in this thread
    # Send updates to client every x seconds.
    #   -> Get updates from database run calculations

    conn = sqlite3.connect('test')
    cur = conn.cursor()

    global flag
    global globalAvgPower
    
    count = 0
    temp = 0
    print (threading.currentThread().getName(), 'Starting')
    while flag:
        data2 = str(round(globalAvgPower,4))
        print (data2)
        print (sys.getsizeof(data2))
        c.send(data2+'\n')
       # print("(txThread) Sent: " + str(count))
       # print("String length: " + str(len(data2.encode('utf-8'))))

        if flag == False:
            c.close()               # Closing connection to client (iOS)
            break
        
        time.sleep(2)
        count += 1

    conn.commit()
    conn.close()
    print (threading.currentThread().getName(), 'Exiting')
# END txThread()

# Main
host = '10.0.8.89'   # Figure out how to get address dynamically
port = 9876
print ("Pi's IP = " + host)

# Create socket
mysocket = socket.socket()
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) # Prevent socket.error: [Errno 98] Address already in use
mysocket.bind((host, port))
mysocket.listen(5)

total_duration = 0

while flag:
    print("Waiting for connection...")
    c, addr = mysocket.accept()

    # Create threads
    db = threading.Thread(name='dbThread', target=dbThread)
    rx = threading.Thread(name='rxThread', target=rxThread)
    tx = threading.Thread(name='txThread', target=txThread)

    # Start threads
    db.start()
    rx.start()
    tx.start()
    
    # Join threads
    db.join()
    rx.join()
    tx.join()

    flag = True

mysocket.close()
GPIO.cleanup()
print ("Server stopped")
