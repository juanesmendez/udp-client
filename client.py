import socket
import pickle
import zlib
import cv2
import struct
import tkinter
from tkinter import messagebox
from os import walk

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, World!"
MESSAGE_2 = "Upload"

BUFFER_SIZE = 4096
BUFFER_FILE = 8192
PAYLOAD_SIZE = struct.calcsize(">L")

TCP_IP = "127.0.0.1"
TCP_PORT = 5014

def receiveVideo(sock, nombreVideo):
    isRecording = True
    while True:
        try:
            print("Recibiendo frame...")
            packetSize, serverAddress = sock.recvfrom(PAYLOAD_SIZE)
            packetSize = struct.unpack(">L", packetSize)

            data = b""
            print("Size:", packetSize[0])
            while len(data) < packetSize[0]:
                newData, serverAddress = sock.recvfrom(BUFFER_SIZE)
                data = data + newData

            print("Actual data size received:", len(data))
            frame = pickle.loads(zlib.decompress(data))

            if isRecording == True:
                cv2.imshow('ImageWindow', frame)

            key = cv2.waitKey(1) & 0xff
            if key == ord('p'):
                print("PAUSE VIDEO")
                while True:

                    key2 = cv2.waitKey(1) or 0xff
                    cv2.imshow('ImageWindow', frame)

                    if key2 == ord('p'):
                        print("PLAY VIDEO")
                        break
            if key == ord('q'):
                sock.sendto("stop".encode(), (UDP_IP, UDP_PORT))
                cv2.destroyAllWindows()
                break
            sendPing(sock)

        except socket.timeout:
            print("Socket timeout.")
            break

    sock.close()
    print("Cerrando socket de transmision streaming...")


def createVideoFile(bytes):
    file = open("video-4.mp4", "wb")
    file.write(bytes)
    file.close()


def sendPing(sock):
    sock.sendto("alive".encode(), (UDP_IP, UDP_PORT))


def uploadVideo(sock, videoPath):
    #Recibir el mensaje del servidor diciendo OK
    print("Uploading video...")
    message, serverAddress = sock.recvfrom(BUFFER_SIZE) #El servidor debe responder con un 'OK'
    print("S:", message.decode())

    sock.sendto("start".encode(), (UDP_IP, UDP_PORT))

    message, serverAddress = sock.recvfrom(BUFFER_SIZE)  # El servidor debe responder con un 'OK'

    #Abrir conexion TCP para enviar archivo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))

    nombre = videoPath.split('/')
    nombre = nombre[len(nombre) - 1]  # Atrapo el nombre del video contenido en el path del mismo

    s.sendall(nombre.encode()) # Se envia el nombre del video

    file = open(videoPath, 'rb')
    data = file.read()
    file.close()

    # Enviar el tamanio del archivo para que el servidor sepa cuanto toca leer
    size = len(data)
    print("Size:", size)
    size = struct.pack(">L", size)
    s.sendall(size)  # Envio el tamaño del video

    s.sendall(data) #Enviamos el archivo

    s.close()
    tkinter.messagebox.showinfo("Estado de solicitud", "El archivo fue recibido exitosamente")


def initializeVideoUpload(videoName, comboFiles):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(MESSAGE_2.encode(), (UDP_IP, UDP_PORT))

    path = './videos/' + videoName
    uploadVideo(sock, path)

    videosList = grabVideosList()
    print(videosList)
    print(type(videosList))
    print("Combo type:", type(comboFiles))
    print("Combo values before,", comboFiles['values'])
    comboFiles['values'] = videosList

def initializeVideoStream(nombreVideo):
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)
    print("message:", MESSAGE)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    # sock.settimeout(3)

    print(f"Video solicitado: {nombreVideo}")

    sock.sendto(nombreVideo.encode(), (UDP_IP, UDP_PORT))

    receiveVideo(sock, nombreVideo)
    # createVideoFile(videoBytes)

    sock.close()


def grabVideosList():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto('videos-list'.encode(), (UDP_IP, UDP_PORT))

    data, serverAddress = sock.recvfrom(BUFFER_SIZE)
    videosList = pickle.loads(data)
    print(videosList)
    return videosList


def grabMyVideosList():
    f = []
    for (dirpath, dirnames, filenames) in walk('./videos'):
        f.extend(filenames)
        break
    print(f)
    return f

#initializeVideoStream('video-5.mp4')
#initializeVideoUpload()
#initializeVideoStream()

