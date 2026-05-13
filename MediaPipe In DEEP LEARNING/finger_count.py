import cv2
import mediapipe as mp

mp_hands=mp.solutions.hands
mp_drawings=mp.solutions.drawing_utils

hands=mp_hands.Hands()

video=cv2.VideoCapture(0)
while True:
    suc,img=video.read()
    img=cv2.flip(img,1)
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(img1)
    # print(result.multi_hand_landmarks)
    tipids=[4,8,12,16,20]
    lmlst=[]
    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            for id,lm in enumerate(handlm.landmark):
                # print(id,lm)
                lmlst.append([id,lm.x,lm.y])
            # print(lmlst)
            if len(lmlst)==21:
                fingerlist=[]
                if lmlst[20][1] > lmlst[8][1]:
                    if lmlst[4][1] > lmlst[3][1]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)
                else:
                    if lmlst[4][1] < lmlst[3][1]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)

                for i in range(1,5):
                    if lmlst[tipids[i]][2]>lmlst[tipids[i]-2][2]:
                        fingerlist.append(0)
                    else:
                        fingerlist.append(1)
                print(fingerlist)
                finger_count=fingerlist.count(1)
                # print(finger_count)
                cv2.putText(img,str(finger_count),(35,400),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),3)
            mp_drawings.draw_landmarks(img,handlm,mp_hands.HAND_CONNECTIONS)
                                    #    mp_drawings.DrawingSpec(color=(255,255,0),
                                    #    circle_radius=4,thickness=2),
                                    #    mp_drawings.DrawingSpec(color=(255,0,0),thickness=2))
    cv2.imshow("WEBCAM",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break
video.release()
cv2.destroyAllWindows()