import math
import time
import cv2
import mediapipe as mp


class handetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=int(self.maxHands), min_detection_confidence=float(self.detectionCon), min_tracking_confidence=float(self.trackCon))
        self.mpDraw = mp.solutions.drawing_utils
        self.tips = [4, 8, 12, 16, 20]  # Indices of fingertips in the landmark list

    def findHands(self, frame, draw=True):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgcolor)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, hand, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNo=0, draw=True):
        xlist = []
        ylist = []
        bbox = []
        self.list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xlist.append(cx)
                ylist.append(cy)
                self.list.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            
            xmin, xmax = min(xlist), max(xlist)
            ymin, ymax = min(ylist), max(ylist)
            bbox = [xmin, ymin, xmax, ymax]
            if draw:
                cv2.rectangle(frame, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)

        return self.list, bbox 
    
    def fingersUp(self):
        fingers = []
        if self.list[self.tips[0]][1] > self.list[self.tips[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

            # Other fingers
        for id in range(1, 5):
            if self.list[self.tips[id]][2] < self.list[self.tips[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
    
    def findDistance(self, p1, p2, frame, draw=True, r=15, t=3):
        x1, y1 = self.list[p1][1:]
        x2, y2 = self.list[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), t)
            cv2.circle(frame, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), r, (0, 255, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, frame, (cx, cy)
    
def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = handetector()

    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        list, bbox = detector.findPosition(frame)
        if len(list) != 0:
            print(list[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(frame, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
        cv2.imshow("Hand Tracking", frame)

        k = cv2.waitKey(1)
        if k == 27:
           break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

    