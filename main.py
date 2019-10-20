from tkinter import *
from tkinter import ttk

from client import *


def buildStreamFrame(root):
    videosList = grabVideosList()


    frame = Frame(root, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=300, height=500)
    frame.pack(side=TOP, fill=BOTH, expand=1)

    label = Label(frame, text="Video Streaming", bg="green", fg="white")
    #label.grid(row=0, columnspan=2, sticky="nsew")
    label.pack(fill=X)

    labelArchivo = Label(frame, text="Seleccione un video:")
    #labelArchivo.grid(row=1, column=0, sticky="W")
    labelArchivo.pack(side=LEFT, fill=X)

    comboArchivo = ttk.Combobox(frame)
    comboArchivo['values'] = videosList
    #comboArchivo.grid(row=2, column=0)
    comboArchivo.pack(side=LEFT, fill=X)

    botonStream = Button(frame, text="Stream", fg="red", command= lambda:initializeVideoStream(comboArchivo.get()))
    #botonDescargar.grid(row=2, column=1)
    botonStream.pack(side=LEFT,fill=X)

    return comboArchivo


def buildUploadVideoFrame(root, comboArchivo):
    videosList = grabMyVideosList()

    frame = Frame(root, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=300, height=500)
    frame.pack(fill=X,  expand=1)

    label = Label(frame, text="Video upload al servidor", bg="blue", fg="white")
    label.grid(row=0, columnspan=3, sticky="nsew")

    labelArchivo = Label(frame, text="Seleccione un video para subir:")
    labelArchivo.grid(row=1, column=0, sticky="W")
    #labelArchivo.pack(side=LEFT)

    comboArchivoServidor = ttk.Combobox(frame)
    comboArchivoServidor['values'] = videosList
    #comboArchivoServidor.pack(side=LEFT)
    comboArchivoServidor.grid(row=1, column=2)


    botonUpload = Button(frame, text="Upload", fg="green", bg="gray", command= lambda: initializeVideoUpload(comboArchivoServidor.get(), comboArchivo))
    # , command= lambda: doTestEvent(comboNumConexiones, comboArchivoServidor)
    #botonRealizarPrueba.pack(side=BOTTOM)
    botonUpload.grid(row=2, columnspan=3)

'''
def buildTestConnectionFrame(root):
    frame = Frame(root)
    frame.pack(side=BOTTOM, fill=BOTH)

    labelTestConnection = Label(frame, text="Test Connection", bg="purple", fg="white")
    labelTestConnection.pack(fill=X)

    botonTestConnection = Button(frame, text="Test Connection", fg="red", command=testConnection)
    #botonTestConnection.grid(columnspan=3)
    botonTestConnection.pack()
'''

def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
#startConnection(0)

root = Tk()
root.title("Aplicacion Streaming")
#center_window(500, 300)
comboArchivo = buildStreamFrame(root)
buildUploadVideoFrame(root, comboArchivo)
#buildTestConnectionFrame(root)

root.mainloop()