import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))
#Lineas de prueba:
modifiedMessage, serverAddress = sock.recvfrom(2048)
print(f"Server address: {serverAddress}")
print(modifiedMessage.decode())
sock.close()