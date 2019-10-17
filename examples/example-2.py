# importing libraries
import cv2
import numpy as np
import pickle
import zlib

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video-4.mp4')

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video  file")

# Read until video is completed
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    bytesFrame = pickle.dumps(frame)
    print("Size frame (bytes):", len(bytesFrame))
    print("Size frame comprimido(bytes):", len(zlib.compress(bytesFrame)))
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    print("Size frame (image)", len(frame))
    if ret == True:

        print(f"Type frame: {type(frame)}")
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()