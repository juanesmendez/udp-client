import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

BUFFER_SIZE = 8192


def receiveVideo(sock):
    packet, serverAddress = sock.recvfrom(BUFFER_SIZE)
    #'''
    sendPing(sock)
    #'''

    print(f"Server address: {serverAddress}")
    videoBytes = b""
    while packet:
        videoBytes = videoBytes + packet
        try:
            print(f"Bytes received: {len(videoBytes)}")
            packet, serverAddress = sock.recvfrom(BUFFER_SIZE)
            #Enviar mensaje al servidor diciendo que sigue en el canal
            #sock.sendto("alive".encode(), (UDP_IP, UDP_PORT))
            #'''
            sendPing(sock)
            #'''
        except socket.timeout:
            print("Socket timeout.")
            break

    print("Continua ejecucion")
    print("Bytes recibidos:", len(videoBytes))
    return videoBytes


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
sock.settimeout(3)

sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

videoBytes = receiveVideo(sock)
createVideoFile(videoBytes)

sock.close()