import cv2
import mediapipe as mp
import numpy as np
import keyboard
import time

max_num_hands = 1

gesture = {
    0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h',
    8:'i', 9:'j', 10:'k', 11:'l', 12:'m', 13:'n', 14:'o', 
    15:'p', 16:'q', 17:'r', 18:'s', 19:'t', 20:'u', 21:'v', 
    22:'w', 23:'x', 24:'y', 25:'z', 26:'spacing', 27:'clear'
}

# mediapipe hand models
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands = max_num_hands,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5)

f = open('test.txt', 'w')

# Make dataSet
file = np.genfromtxt('dataSet.txt', delimiter=',')
angleFile = file[:,:-1]
labelFile = file[:,-1]
angle = angleFile.astype(np.float32)
label = labelFile.astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)
cap = cv2.VideoCapture(0)

startTime = time.time()
prev_index = 0
sentence = ''
recognizeDelay = 1
while True:
    ret, img = cap.read()
    if not ret:
        continue
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BAYER_BG2BGR)
    result = hands.process(imgRGB)

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeors((21,3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            v1 = joint[[0,1,2,3, 0,5,6,7, 0,9,10,11, 0,13,14,15, 0,17,18,19],:] # 손가락
            v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],:]  # 마디

            v = v2 - v1
            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]
            compareV1 = v[[0,1,2,3,4,5,6,7,8,9,10,12,13,14,16,17],:]
            compareV2 = v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:]

            angle = np.degrees(angle)
            if keyboard.is_pressed('a'):    # a를 누를시 현재 데이터(angle)가 txt파일에 저장됨
                for num in angle:
                    num = round(num,6)
                    f.write(str(num))
                    f.write(',')
                f.wrtie("27.000000")        # 데이터를 저장할 gesture의 label번호
                f.write(',')
                print("next")
            data = np.array([angle], dtype=np.float32)
            ret, result, neighbours, dist = knn.findNearest(data,3)
            index = int(result[0][0])
            if index != prev_index:
                startTime = time.time()
                prev_index = index
            else:
                if time.time() - startTime > recognizeDelay:
                    if index == 26:
                        sentence += ' '
                    elif index == 27:
                        sentence = ''
                    else:
                        sentence += gesture[index]
                    startTime = time.time()

            cv2.putText(img, gesture[index].upper(), (int(res.landmark[0].x * img.shape[1] - 10),int(res.landmark[0].y * img.shape[0] + 40)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        
        mp_drawing.draw_landmarks(img,res,mp_hands.HAND_CONNECTIONS)
    cv2.putText(img, sentence,(20,440), cv2.FONT_HERSHEY_SIMPLEX,2, (255,255,255), 3)

    cv2.imshow("HandTracking",img)
    cv2.waitKey(1)
    if keyboard.is_pressed('b'): #b를 누를시 프로그램 종료
        break
f.close()

