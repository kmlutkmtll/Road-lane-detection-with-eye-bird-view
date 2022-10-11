import cv2
import numpy as np

cap = cv2.VideoCapture("test2.mp4")

lineLeft = []
lineRight = []
lineMiddle = []
centerAll = []
centerLeft = []
centerRight = []

while True:
    _,frame = cap.read()
    frame = cv2.resize(frame,(1280,720))

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    height = 480
    width = 640

    pts1 = np.float32([[250,400],[45,475],[720,400],[830,475]])
    pts2 = np.float32([[0,0],[0,height],[width,0],[width,height]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    warp = cv2.warpPerspective(gray,M,(width,height))
    eye_bird = cv2.warpPerspective(frame,M,(width,height))

    # gb = cv2.GaussianBlur(eye_bird,(7,7),0)
    # blur = cv2.blur(gb,(7,7))
    edges = cv2.Canny(eye_bird,50,70)

    theta = np.pi / 180

    min_line_len = 150
    max_line_gap = 60

    lines = cv2.HoughLinesP(edges,1,theta,100,np.array([]),130,50)

    for line in lines:

        # 330 lar ortadaki
        for x1, y1, x2, y2 in line:
            cv2.line(eye_bird,(x1,y1),(x2,y2),(0,255,0),5)
            # print(x2)

        if (x1>40 and x1 < 120):
            lineLeft.append(x1)
            # lineLeft.sort()
        elif (x1 > 500 and x1 < 600):
            lineRight.append(x1)
            # lineRight.sort()
        else:
            lineMiddle.append(x1)
            # lineMiddle.sort()
        print(lineLeft)

        leftMean = np.mean(lineLeft)
        middleMean = np.mean(lineMiddle)
        rightMean = np.mean(lineRight)

        betweenLeftAndMiddle = (leftMean + middleMean) / 2
        betweenLeftAndMiddle = np.nan_to_num(betweenLeftAndMiddle)
        betweenLeftAndMiddle = betweenLeftAndMiddle.astype(int)

        betweenRightAndMiddle = (rightMean + middleMean) / 2
        betweenRightAndMiddle = np.nan_to_num(betweenRightAndMiddle)
        betweenRightAndMiddle = betweenRightAndMiddle.astype(int)

        print(betweenLeftAndMiddle)
        print(betweenRightAndMiddle)

        cv2.circle(eye_bird,(betweenRightAndMiddle+15,250),10,(0,0,255),cv2.FILLED)
        cv2.putText(eye_bird,"Center Right",(betweenRightAndMiddle+15,230),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0))

        cv2.circle(eye_bird,(betweenLeftAndMiddle+15,250),10,(0,0,255),cv2.FILLED)
        cv2.putText(eye_bird, "Center Left", (betweenLeftAndMiddle + 15, 230), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0))


    cv2.imshow("saas",eye_bird)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()