import cv2
import numpy as np
import followhands as fh
import autopy
import pyautogui

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

# Left click with index and thumb
        if fingers[1] == 1 and fingers[0] == 1:  # Índice y pulgar levantados
            length, frame, center = detector.findDistance(8, 4, frame)
            cv2.line(frame, (list[8][1], list[8][2]), (list[4][1], list[4][2]), (0, 255, 0), 3)
            if length < 40:
                cv2.circle(frame, center, 10, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.LEFT)

        # Right click with index and middle finger
        if fingers[1] == 1 and fingers[2] == 1:  # Índice y medio levantados
            length, frame, center = detector.findDistance(8, 12, frame)
            cv2.line(frame, (list[8][1], list[8][2]), (list[12][1], list[12][2]), (255, 0, 0), 3)
            if length < 20:
                cv2.circle(frame, center, 10, (255, 0, 0), cv2.FILLED)
                autopy.mouse.click(autopy.mouse.Button.RIGHT)


                
        if all(f == 0 for f in fingers):  # Mano cerrada (puño)
            pyautogui.scroll(-50)  # Scroll hacia abajo
        elif all(f == 1 for f in fingers):  # Mano completamente abierta
            pyautogui.scroll(50)   # Scroll hacia arriba

            
    cv2.imshow("Virtual Mouse", frame)
    k = cv2.waitKey(1)
    if k == 27:  
        break

cap.release()
cv2.destroyAllWindows()

        