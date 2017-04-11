import socket
import threading
import time
import RPi.GPIO as GPIO # Import GPIO Library

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

def rxThread():
    # Receive/Read message in this thread
    # Outlet Control
    #   -> Code to turn on and off the RPi's pins here
    print (threading.currentThread().getName(), 'Starting')

    while flag:
        data = c.recv(1024)
        data = data.decode("utf-8")
        if data == '':
            continue
        else:
            print ("\n(rxThread) Recieved: " + data + " from " + addr[0])

        if data == "QUIT":
            GPIO.cleanup()
            break

        if data == "LED1:on":
            GPIO.output(pin1, True)
        if data == "LED2:on":
            GPIO.output(pin2, True)
        if data == "LED3:on":
            GPIO.output(pin3, True)
        if data == "LED4:on":
            GPIO.output(pin4, True)

        if data == "LED1:off":
            GPIO.output(pin1, False)
        if data == "LED2:off":
            GPIO.output(pin2, False)
        if data == "LED3:off":
            GPIO.output(pin3, False)
        if data == "LED4:off":
            GPIO.output(pin4, False)

    print (threading.currentThread().getName(), 'Exiting')
# END rxThread()

def txThread():
    # Transmit/Send message in this thread
    # Send updates to client every x seconds.
    #   -> Get updates from database run calculations
    count = 0
    print (threading.currentThread().getName(), 'Starting')
    while flag:
        data2 = str(count)
        data2 = data2.encode()
        c.send(data2)
        print("(txThread) Sent: " + str(count))
        print("String length: " + str(len(data2.encode('utf-8'))))

        if flag == False:
            break
        time.sleep(2)
        count = count + 1

    print (threading.currentThread().getName(), 'Exiting')
# END txThread()

# Main
host = '10.0.8.143'   # Figure out how to get address dynamically
port = 9876
print ("Pi's IP = " + host)

flag = True     # flag to control threads

# Create socket
mysocket = socket.socket()
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Prevent socket.error: [Errno 98] Address already in use
mysocket.bind((host, port))
mysocket.listen(5)
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

print ("Server stopped")
c.close()
