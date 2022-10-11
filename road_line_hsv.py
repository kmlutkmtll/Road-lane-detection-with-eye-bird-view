import cv2
import numpy as np

cap = cv2.VideoCapture("road.mp4")

while True:
    _,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(frame,cv2.COLOR_RGB2HSV)
    lower_yellow = np.array([20,100,100],dtype="uint8")
    upper_yellow = np.array([30,255,255],dtype="uint8")

    mask_yellow = cv2.inRange(hsv,lower_yellow,upper_yellow)
    mask_white = cv2.inRange(gray,200,255)
    mask_yw = cv2.bitwise_or(mask_white,mask_yellow)
    mask_yw_frame = cv2.bitwise_and(gray,mask_yw)

    # blur = cv2.blur(gray,(5,5))
    gb = cv2.GaussianBlur(gray,(5,5),0)

    median = np.median(gb)
    low = int(max(0, (1 - 0.33) * median))
    high = int(min(255, (1 + 0.33) * median))

    edges = cv2.Canny(gb,50,150)

    # cv2.imshow("edges",edges)
    cv2.imshow("last",mask_yw_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
