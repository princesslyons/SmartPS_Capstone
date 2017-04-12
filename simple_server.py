import socket
import threading
import time
import RPi.GPIO as GPIO # Import GPIO Library
import sqlite3
import datetime

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

flag = True     # flag to control thread

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
        else:
            print ("\n(rxThread) Recieved: " + data + " from " + addr[0])

        if data == "QUIT":
            GPIO.output(pin1, 0)
            GPIO.output(pin2, 0)
            GPIO.output(pin3, 0)
            GPIO.output(pin4, 0)
            #GPIO.cleanup()
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

    #conn = sqlite3.connect('test')
    #cur = conn.cursor()

    global flag
    
    count = 0
    print (threading.currentThread().getName(), 'Starting')
    while flag:
        data2 = str(count)
        data2 = data2.encode()
        c.send(data2)
        print("(txThread) Sent: " + str(count))
        print("String length: " + str(len(data2.encode('utf-8'))))

        if flag == False:
            c.close()               # Closing connection to client (iOS)
            break
        
        time.sleep(2)
        count = count + 1

    #conn.commit()
    #conn.close()
    print (threading.currentThread().getName(), 'Exiting')
# END txThread()

# Main
host = '10.0.8.43'   # Figure out how to get address dynamically
port = 3000
print ("Pi's IP = " + host)

# Create socket
mysocket = socket.socket()
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1) # Prevent socket.error: [Errno 98] Address already in use
mysocket.bind((host, port))
mysocket.listen(5)

total_duration = 0
#db = threading.Thread(name='dbThread', target=dbThread)

while flag:
    print("Waiting for connection...")
    c, addr = mysocket.accept()

    # Create threads
    rx = threading.Thread(name='rxThread', target=rxThread)
    tx = threading.Thread(name='txThread', target=txThread)

    # Start threads
    rx.start()
    tx.start()
    
    # Join threads
    rx.join()
    tx.join()

    flag = True

mysocket.close()
GPIO.cleanup()
print ("Server stopped")
