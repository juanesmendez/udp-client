import socket
import pickle
import zlib
import cv2
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

BUFFER_SIZE = 8192
PAYLOAD_SIZE = struct.calcsize(">L")

def receiveVideo(sock):
    while True:
        try:
            packetSize, serverAddress = sock.recvfrom(PAYLOAD_SIZE)
            packetSize = struct.unpack(">L", packetSize)

            #print("Packet size", packetSize[0])
            #print("Packet size type", type(packetSize[0]))
            data = b""
            while len(data) < packetSize[0]:
                newData, serverAddress = sock.recvfrom(BUFFER_SIZE)
                #print(f"Receiving data: {newData}")
                data = data + newData
                #print("Total data received:", len(data))

            frame = pickle.loads(zlib.decompress(data))
            #print(frame)

            #frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('ImageWindow', frame)
            cv2.waitKey(1)

            sendPing(sock)

        except socket.timeout:
            print("Socket timeout.")
            break




def createVideoFile(bytes):
    file = open("video-4.mp4", "wb")
    file.write(bytes)
    file.close()


def sendPing(sock):
    sock.sendto("alive".encode(), (UDP_IP, UDP_PORT))


print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#sock.settimeout(3)

sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

receiveVideo(sock)
#createVideoFile(videoBytes)

sock.close()

'''
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''
