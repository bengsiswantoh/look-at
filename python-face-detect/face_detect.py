import cv2 as cv

import socket
import json

face_cascade = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

cap = cv.VideoCapture(0)

opened_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
scale = 100
recording = 1

while(cap.isOpened()):
  ret, frame = cap.read()

  width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
  height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  #face_detect = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
  face_detect = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

  for (x, y, w, h) in face_detect:
    #print(x, y, w, h)
    #roi_gray = gray[y:y+h, x:x+w]
    #roi_color = frame[y:y+h, x:x+w]

    color = (255, 0, 0)
    stroke = 2
    end_cord_x = x+w
    end_cord_y = y+h
    #cv.rectangle(frame, (x, y), (end_cord_y, end_cord_y), color, stroke)

    center_cord_x = x+w/2
    center_cord_y = y+h/2

    adjust_crod_x = (center_cord_x-width/2)*recording/scale
    adjust_crod_y = (center_cord_y-height/2)*-1/scale

    position = {"x": adjust_crod_x, "y": adjust_crod_y}

    byte_message = bytes(json.dumps(position), "utf-8")
    opened_socket.sendto(byte_message, ("127.0.0.1", 3000))
    print(json.dumps(position))

  cv.imshow("Frame", frame)

  if cv.waitKey(20) & 0xFF == ord("q"):
    break

cap.release()
cv.destroyAllWindows()
opened_socket.close()