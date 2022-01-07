#sign_test

#import
import cv2
import mediapipe as mp
import math
import test
import mouse

# variable
max_num_hands = 1

# cam
cap = cv2.VideoCapture(0)

# mediapipe soulutins
mpHands = mp.solutions.hands
my_hands = mpHands.Hands(max_num_hands = max_num_hands,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5)
mpDraw = mp.solutions.drawing_utils
    
# distance
def dist(x1,y1,x2,y2):
    return math.sqrt(math.pow(x1-x2, 2)) + math.sqrt(math.pow(y1-y2,2))

# finger
compareIndex = [[5,4],[6,8],[10,12],[14,16],[18,20]]

# thumb, index_finger, middle_finger, ring_figer, pinky (엄지 검지 중지 약지 소지)
open = [False,False,False,False,False]
gesture =  [[False,True,False,False,False,'1'],
            [False,True,True,False,False,'2'],
            [True,True,True,False,False,'3'],
            [False,True,True,True,True,'4'],
            [True,True,True,True,True, '5']]


# angle
while True:
    success, img = cap.read()
    h,w,c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for i in range(0,5):
                open[i] = dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[compareIndex[i][0]].x, handLms.landmark[compareIndex[i][0]].y) < \
                dist(handLms.landmark[0].x, handLms.landmark[0].y, handLms.landmark[compareIndex[i][1]].x, handLms.landmark[compareIndex[i][1]].y)

        print(open)
        text_x = (handLms.landmark[0].x * w)
        text_y = (handLms.landmark[0].y * h)
        for i in range(0, len(gesture)):
            flag = True
            for j in range(0,5):
                if(gesture[i][j] != open[j]):
                    flag = False
            if(flag ==True):
                cv2.putText(img, gesture[i][5], (round(text_x)-50, round(text_y)-250),
                            cv2.FONT_HERSHEY_PLAIN,4,(0,0,0),4)
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # reversal
    fimg = cv2.flip(img,1)

    # show img(cam)
    cv2.imshow("MAIN",fimg)
    if open == [False,True,False,False,False]:
        cv2.destroyWindow('MAIN')
        test.one()
        

    if open == [False,True,True,False,False]:
        cv2.destroyWindow('MAIN')
        mouse.two()
        
        
    if cv2.waitKey(1) == ord('q'):
        break

    import random

q = list(0 for i in range(5))
qc = list(0 for i in range(5))

for i in range(20):
    num = random.randrange(1, 101)
    if i<5: #0~4까지 랜덤한수 넣기
        q[i] = chr(num)
        print(q)
    else:
        for j in range(4): #좌로 밀어주기
            qc[j] = q[j + 1]
        q[4] = chr(num)
        q = qc
        print(q)