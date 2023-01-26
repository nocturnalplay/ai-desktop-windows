import mediapipe as mp
import cv2
import autopy
import numpy as np
import math

############################
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
wScr, hScr = autopy.screen.size()
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7
frameR = 100
#############################


with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                x1 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                y1 = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                xd = x * 1920
                yd = y * 1080
                x1d = x1 * 1920
                y1d = y1 * 1080
                dist = math.hypot(x1d - xd, y1d - yd)
                h, w, c = image.shape
                x, y = int(x * w), int(y * h)
                cv2.rectangle(image, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                x = np.interp(x, (frameR, wCam - frameR), (0, wScr))
                y = np.interp(y, (frameR, hCam - frameR), (0, hScr))
                clocX = plocX + (x - plocX) / smoothening
                clocY = plocY + (y - plocY) / smoothening
                clocX = round(clocX, 0)
                clocY = round(clocY, 0)
                try:
                    autopy.mouse.move(clocX, clocY)
                    plocX, plocY = clocX, clocY
                except ValueError:
                    plocX, plocY = clocX, clocY
                    continue
                autopy.mouse.move(clocX, clocY)
                dist = dist / 100
                dist = round(dist, 0)
                if dist < 3:
                    autopy.mouse.click()
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
