import cv2
import mediapipe as mp
import time
import os
import HandTrackingModule as htm


cam = cv2.VideoCapture(0) #
hands = mp.solutions.hands.Hands(max_num_hands=1) #Объект ИИ для определения ладони; их количество
draw_h = mp.solutions.drawing_utils #Для рисование ладони

folderPath = "fingers"
fingerList = os.listdir(folderPath)
overlayList = []
for imgPath in fingerList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    overlayList.append(image)

pTime = 0

detector = htm.handDetector(detectionCon=0.75, maxHands=1)
totalFingers = 0

while True:

    if cv2.waitKey(1) & 0xFF == 27:
        break

    sucess, img = cam.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)

    if lmList:
        fingersUp = detector.fingersUp()
        totalFingers = fingersUp.count(1)

    h, w, c = overlayList[totalFingers].shape
    img[0:h, 0:w] = overlayList[totalFingers]

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cv2.imshow("Image", img)







