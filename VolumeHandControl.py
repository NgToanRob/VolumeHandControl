import cv2
import mediapipe as mp
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()


# Setup camera
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#Set model
tracker = htm.Tracker(mode= True, maxHands=1, detCon=0.6, traCon=0.6)

# set volume
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
volMin, volMax = volRange[0], volRange[1]

volNow = volume.GetMasterVolumeLevel()
# set defalt color and volume percents
percent = np.interp(volNow, [volMin, volMax], [0,100])
redColor = np.interp(percent, [0, 70], [0, 255])
greenColor = np.interp(percent, [70, 100], [255, 0])
perHigh = int(np.interp(percent, [0, 100], [440, 300]))
if percent <=70:
    color = (0, 255, redColor)
else:
    color = (0, greenColor, 255)





timer = cv2.getTickCount()
while True:
    success, img = cap.read()
    # run model
    img, landmarks = tracker.findHands(img)

    if len(landmarks) == 0:
        cv2.rectangle(img, (570, 300), (600, 440), color, 1)
        cv2.rectangle(img, (570, perHigh), (600, 440), color, cv2.FILLED)
        cv2.putText(img, f"{int(percent)}%", (550, 280),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    # Take the position of the index finger (=4) and thumb (=8) in landmarks
    if len(landmarks) != 0:

        x1, y1 = landmarks.get(4)[0], landmarks.get(4)[1]
        x2, y2 = landmarks.get(8)[0], landmarks.get(8)[1]
        xc, yc = (x1+x2) // 2 , (y1+y2) // 2

        length = int(math.hypot(x2-x1, y2-y1))

        # Hand range 50 - 300
        # Volume range -65.25  - 0
        # convert lenght to vol
        vol_num = np.interp(length, [30,200], [volMin, volMax])

        # convert lenght to percent
        percent = np.interp(length, [30,200], [0,100]); print(int(percent))
        redColor = np.interp(percent, [0,70], [0,255])
        greenColor = np.interp(percent, [70,100], [255,0])

        # convert percent to percent high
        perHigh = np.interp(percent, [0,100], [440,300])

        # cv2.putText(img, f"{int(percent)}%", (600,280), cv2.FONT_HERSHEY_SIMPLEX, 0.75, )
        if length < 30:
            # nhỏ hơn 50 tô màu xanh
            perHigh = 440
            color = (0,255,0)

            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.circle(img, (xc, yc), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            cv2.rectangle(img, (570, 300), (600, 440), color, 1)
            cv2.rectangle(img, (570, perHigh), (600, 440), color, cv2.FILLED)
            cv2.putText(img, f"{int(percent)}%", (550, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            volume.SetMasterVolumeLevel(volMin, None)

        if length > 200:
            # lớn hơn 300 tô màu đỏ
            perHigh = 300
            color = (0, 0, 255)
            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.circle(img, (xc, yc), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            cv2.rectangle(img, (570, 300), (600, 440), color, 1)
            cv2.rectangle(img, (570, perHigh), (600, 440), color, cv2.FILLED)
            cv2.putText(img, f"{int(percent)}%", (550, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            volume.SetMasterVolumeLevel(volMax, None)

        if percent <= 70:
            perHigh = int(np.interp(percent, [0, 100], [440, 300]))
            color = (0, 255, redColor)
            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.circle(img, (xc, yc), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            cv2.rectangle(img, (570, 300), (600, 440), color, 1)
            cv2.rectangle(img, (570, perHigh), (600, 440), color, cv2.FILLED)
            cv2.putText(img, f"{int(percent)}%", (550, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            volume.SetMasterVolumeLevel(vol_num, None)

        if percent > 70:
            perHigh = int(np.interp(percent, [0, 100], [440, 300]))
            color = (0, greenColor, 255)
            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.circle(img, (xc, yc), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)

            cv2.rectangle(img, (570, 300), (600, 440), color, 1)
            cv2.rectangle(img, (570, perHigh), (600, 440), color, cv2.FILLED)
            cv2.putText(img, f"{int(percent)}%", (550, 280),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

            volume.SetMasterVolumeLevel(vol_num, None)

    # Get FPS
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    timer = cv2.getTickCount()
    cv2.putText(img, "FPS : " + str(int(fps)), (40, 40),
                cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2);
    cv2.putText(img,"Adjust the volume with your one hand", (40, 60),
                cv2.FONT_HERSHEY_DUPLEX, 0.75, (255, 255, 255), 2);
    cv2.imshow('Video', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()