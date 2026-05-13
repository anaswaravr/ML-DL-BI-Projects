
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

    tipids=[4,8,12,16,20]
    lmlst=[]

    if result.multi_hand_landmarks:
        for handlm in result.multi_hand_landmarks:
            lmlst=[]   # reset list for each hand

            for id,lm in enumerate(handlm.landmark):
                lmlst.append([id,lm.x,lm.y])

            if len(lmlst)==21:
                fingerlist=[]

                # Thumb (Left/Right safe logic)
                if lmlst[20][1] > lmlst[8][1]:
                    if lmlst[4][1] > lmlst[3][1]:
                        fingerlist.append(1)
                    else:
                        fingerlist.append(0)
                else:
                    if lmlst[4][1] < lmlst[3][1]:
                        fingerlist.append(1)
                    else:
                        fingerlist.append(0)

                # Other fingers
                for i in range(1,5):
                    if lmlst[tipids[i]][2] < lmlst[tipids[i]-2][2]:
                        fingerlist.append(1)
                    else:
                        fingerlist.append(0)

                print(fingerlist)

                finger_count=fingerlist.count(1)

                # =====================================
                # ✋ GESTURE DETECTION (ADDED PART)
                # =====================================

                gesture=""

                # 👍 THUMBS UP (Only thumb up)
                if fingerlist == [1,0,0,0,0]:
                    gesture="THUMBS UP"

                # ✌ PEACE (Index & Middle up)
                elif fingerlist == [0,1,1,0,0]:
                    gesture="PEACE"

                # 🤟 ROCK (Thumb, Index, Pinky up)
                elif fingerlist == [1,1,0,0,1]:
                    gesture="ROCK"
                # gesture="UNKNOWN"

# # 👍 THUMBS UP
#                 if fingerlist[0]==1 and finger_count==1:
#                     gesture="THUMBS UP"

# # ✌ PEACE
#                 elif fingerlist[1]==1 and fingerlist[2]==1 and finger_count==2:
#                     gesture="PEACE"

# # 🤟 ROCK
#                 elif fingerlist[0]==1 and fingerlist[1]==1 and fingerlist[4]==1 and finger_count==3:
#                      gesture="ROCK"

                cv2.putText(img,gesture,(35,400),
                            cv2.FONT_HERSHEY_COMPLEX,
                            2,(0,255,0),3)

            mp_drawings.draw_landmarks(img,handlm,mp_hands.HAND_CONNECTIONS)

    cv2.imshow("WEBCAM",img)

    if cv2.waitKey(1) & 0XFF==ord('q'):
        break

video.release()
cv2.destroyAllWindows()