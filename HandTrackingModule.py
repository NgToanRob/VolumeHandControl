import  cv2
import mediapipe as mp
import time

class Tracker():
    def __init__(self, mode=False, maxHands=2, detCon=0.5, traCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detCon = detCon
        self.traCon  = traCon

        self.mpHand = mp.solutions.hands
        self.hands = self.mpHand.Hands(self.mode, self.maxHands, self.detCon, self.traCon)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawSpec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=3)

    def findHands(self, img, draw=True):
        landmarks = {}
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, landmark in enumerate(handLms.landmark):
                    l, w, _ = img.shape
                    landmarks[id] = [int(landmark.x*w), int(landmark.y*l), int(landmark.z*w)]
                if draw:
                    self.mp_drawing.draw_landmarks(img, handLms, self.mpHand.HAND_CONNECTIONS, self.drawSpec, self.drawSpec )
        return img, landmarks

    def findPositions(self, img, handNo=0):
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    l, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * l)
                    if id == handNo:
                        cv2.circle(img, (cx, cy), 20, (155, 249, 255), thickness=1)

def main():
    cap = cv2.VideoCapture(0)
    tracker = Tracker()
    while True:
        success, img = cap.read()
        timer = cv2.getTickCount()

        # print(results.multi_hand_landmarks)
        img = tracker.findHands(img)
        # tracker.findPositions(img, handNo=4)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(img, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
