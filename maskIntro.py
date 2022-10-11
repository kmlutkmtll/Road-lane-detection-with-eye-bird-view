import cv2
import numpy as np

cap = cv2.VideoCapture("road.mp4")

while True:
    _,frame = cap.read()
    frame = np.asarray(frame)
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    gb = cv2.GaussianBlur(gray,(5,5),0)
    edges = cv2.Canny(gb,50,150)

    height,width = frame.shape[0:2]
    # print(height,width)
    triangle = np.array([[(100,height),(475,325),(width,height)]])
    mask = np.zeros_like(frame)
    mask = cv2.fillPoly(mask,triangle,255)
    mask = cv2.bitwise_and(frame,mask)

    cv2.imshow("mask",mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

