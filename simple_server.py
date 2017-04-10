import socket
import threading
import time

# 1. Needs to know if a client is connected
# 2. How to SEND data? - remember it's sent as bytes
# 3. Remove the b'....' from the incoming message

# http://studyswift.blogspot.com/2016/03/communication-between-ios-device-client.html

def rxThread():
    # Receive/Read message in this thread
    # Outlet Control
    #   -> Code to turn on and off the RPi's pins here
    print (threading.currentThread().getName(), 'Starting')

    while flag:
        #print ("(rxThread) Waiting on data...")
        data = c.recv(1024)
        data = data.decode("utf-8")
        if data == '':
            continue
        else:
            inputStr = "\n(rxThread) Recieved: " + data + " from " + addr[0]
            print (inputStr)

        if flag == False:
            break

    print (threading.currentThread().getName(), 'Exiting')
# END rxThread()

def txThread():
    # Transmit/Send message in this thread
    # Send updates to client every x seconds.
    #   -> Get updates from database run calculations
    count = 0
    print (threading.currentThread().getName(), 'Starting')
    while flag:
        #data2 = "[SENDING POWER STRIP INFORMATION]"
        data2 = str(count)
        data2 = data2.encode()
        c.send(data2)
        print("(txThread) Sent: " + str(count))

        if flag == False:
            break
        time.sleep(5)
        count = count + 1

    print (threading.currentThread().getName(), 'Exiting')
# END txThread()

# Main
host = '192.168.2.6'   # Figure out how to get address dynamically
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
