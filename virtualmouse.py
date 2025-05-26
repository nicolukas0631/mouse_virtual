import cv2
import numpy as np
import followhands as fh
import autopy

wcam, hcam = 640, 480
chart = 100
wscreen, hscreen = autopy.screen.size()
sua = 5
pubix, pubiy = 0, 0
cubix, cubiy = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
detector = fh.handetector(maxHands=1)
while True:
    # Read frame from webcam and process it with the hand detector
    ret, frame = cap.read()
    frame = detector.findHands(frame)
    list, bbox = detector.findPosition(frame, draw=False)

    #   Process the index and middle finger tips
    if len(list) != 0:
        x1, y1 = list[8][1], list[8][2]  # Index finger tip
        x2, y2 = list[12][1], list[12][2]  # Middle finger tipip

        fingers = detector.fingersUp()
        cv2.rectangle(frame, (chart, chart), (wcam - chart, hcam - chart), (10, 10, 10), 2)

        if fingers[1] == 1 and fingers[2] == 0:  # Index finger up

            x3 = np.interp(x1, (chart, wcam - chart), (0, wscreen))
            y3 = np.interp(y1, (chart, hcam - chart), (0, hscreen))

            cubix = pubix + (x3 - pubix) / sua
            cubiy = pubiy + (y3 - pubiy) / sua

            autopy.mouse.move(wscreen - cubix, cubiy)
            cv2.circle(frame, (x1, y1), 15, (0, 0, 0), cv2.FILLED)
            pubix, pubiy = cubix, cubiy

        if fingers[1] == 1 and fingers[2] == 1:  # Both fingers up

            length, frame, center = detector.findDistance(8, 12, frame)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            print(length)

            if length < 40:  # If fingers are close enough
                cv2.circle(frame, center, 10, (0, 0, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.LEFT)

    cv2.imshow("Virtual Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:  
        break

cap.release()
cv2.destroyAllWindows()

        