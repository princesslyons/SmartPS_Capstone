import socket
import thread
import time

# 1. Needs to know if a client is connected
# 2. How to SEND data? - remember it's sent as bytes
# 3. Remove the b'....' from the incoming message

# http://studyswift.blogspot.com/2016/03/communication-between-ios-device-client.html

def sendMsg(msg,delay):
    while 1:
        print msg
        # data2 = "[SENDING POWER STRIP INFORMATION]"
        # message = "\nPython(server) to Swift(client)\n" + "\tFrom server at " + addr[0] + ": " + data2 + "\n"
        # message = message.encode()
        # c.send(message)
        time.sleep(delay)

mysocket = socket.socket()
host = '100.65.1.12'   # Figure out how to get address dynamically - ...iPhone app needs it too though
port = 9876

#if host == "127.0.1.1":
#    import commands
#    host = commands.getoutput("hostname -I")
print ("Pi's IP = " + host)

#Prevent socket.error: [Errno 98] Address already in use
mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

mysocket.bind((host, port))

mysocket.listen(5)

c, addr = mysocket.accept()

try:
    thread.start_new_thread(sendMsg, ("Second thread!!!",2))
except:
    print "Error threading"

while True:
    print ("Waiting on data...")
    data = c.recv(1024)
    #data = data.replace("\r\n", '') #remove new line character
    inputStr = "\nSwift(client) to Python(server)\n" + "\tFrom client at " + addr[0] + ": " + str(data)
    print (inputStr)
    # data2 = "[SENDING POWER STRIP INFORMATION]"
    # message = "\nPython(server) to Swift(client)\n" + "\tFrom server at " + addr[0] + ": " + data2 + "\n"
    # message = message.encode()
    # c.send(message)

    if data == "Quit": break

#c.send("Server stopped\n")
print ("Server stopped")
c.close()
