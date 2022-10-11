import cv2
import numpy as np

cap = cv2.VideoCapture("test2.mp4")

while True:
    _,frame = cap.read()
    # gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    height = 480
    width = 640

    pts1 = np.float32([[250,400],[45,475],[720,400],[830,475]])
    pts2 = np.float32([[0,0],[0,height],[width,0],[width,height]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    warp = cv2.warpPerspective(frame,M,(width,height))
    eye_bird = cv2.warpPerspective(frame,M,(width,height))
    eye_bird_gray = cv2.cvtColor(eye_bird,cv2.COLOR_BGR2GRAY)

    gb = cv2.GaussianBlur(eye_bird_gray,(7,7),0)
    blur = cv2.blur(gb,(7,7))
    edges = cv2.Canny(blur,20,40)

    theta = np.pi / 180

    min_line_len = 150
    max_line_gap = 60

    lines = cv2.HoughLinesP(edges,3,theta,15,np.array([]),150,60)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(eye_bird,(x1,y1),(x2,y2),(0,255,0),5)




    cv2.imshow("saas",eye_bird_gray)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()