import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture("road.mp4")

while True:
    _,frame = cap.read()

    frame_h = 223
    frame_w = 950

    src = np.float32([[0, frame_h], [1207, frame_h], [0, 0], [frame_w, 0]])
    dst = np.float32([[569, frame_h], [711, frame_h], [0, 0], [frame_w, 0]])
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)

    frame = frame[450:(450 + frame_h), 0:frame_w]
    warped_frame = cv2.warpPerspective(frame, M, (frame_w, frame_h))

    frame_inv = cv2.warpPerspective(warped_frame, Minv, (frame_w, frame_h))

    gray = cv2.cvtColor(frame_inv, cv2.COLOR_BGR2GRAY)
    gb = cv2.GaussianBlur(gray, (7, 7), 0)
    blur = cv2.blur(gb,(10,10))
    edges = cv2.Canny(blur, 20, 40)

    height = frame.shape[0]
    triangle = np.array([(200,height),(1100,height),(550,250)])

    rho = 1
    theta = np.pi / 180
    threshold = 100
    min_line_len = 130
    max_line_gap = 50
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)

    for line in lines:
        print(len(lines))
        for x1, y1, x2, y2 in line:
            cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 5)



    cv2.imshow("das", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()