import cv2
import mediapipe as mp
import time
import numpy as np
from cvzone.FaceMeshModule import FaceMeshDetector
import cvzone
import os 
import random
# there are total 468 landmark points on the face
cap=cv2.VideoCapture(0)
cap.set(3,1280)                        # width
cap.set(4,720)                         # height
detector = FaceMeshDetector(maxFaces=1)
idlist=[0,17,78,292]  #[lower,upper,left,right]

# import images 
folderEatable ='Objects/eatable'                            # address
listEatable = os.listdir(folderEatable)
print(listEatable)
eatables =[]
for object in listEatable:
    eatables.append(cv2.imread(f'{folderEatable}/{object}',cv2.IMREAD_UNCHANGED))


folderNonEatable ='Objects/noneatable'                            # address
listNonEatable = os.listdir(folderNonEatable)
print(listNonEatable)
Noneatables =[]
for object in listNonEatable:
    Noneatables.append(cv2.imread(f'{folderNonEatable}/{object}',cv2.IMREAD_UNCHANGED))
    
currentObjects= eatables[0]
pos= [300,0]
speed= 5                                 # to move object 5 pixels each iteration
count=0
global isEatable
isEatable =True
gameOver=False

def resetObject():
    global isEatable
    pos[0]= random.randint(100,1180)
    pos[1]= 0
    randNO=random.randint(0,2)                   #change the ratio to choose eatables vs non-eatables
    if randNO==0:
        currentObjects=Noneatables[random.randint(0,3)]
        isEatable=False
    else:
        currentObjects=eatables[random.randint(0,3)]
        isEatable=True
    
    return currentObjects

while True:
    sucess, img=cap.read()
    img = cv2.flip(img, 1)
    if gameOver is False:
        img,faces=detector.findFaceMesh(img,draw=False)          #draw=False(to remove other all point from the face )
    
        img=cvzone.overlayPNG(img,currentObjects,pos)
        pos[1] +=speed
    
        if pos[1]>620:
            currentObjects=resetObject()
    
        if faces:
            face= faces[0]              #gives the coordinates of 468 key points on the detected face in the form of a list of tuples, each representing a (x, y) coordinate.
    #to find which co-ordinates belongs to which id 
    # to find the id of lips
    #    for idNo, point  in enumerate(face):
    #       cv2.putText(img,str(idNo),point,cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7,(255,0,255),1)  
    
        up= face[idlist[0]]
        down=face[idlist[1]]
        for id in idlist:
            cv2.circle(img,face[id],5,(255,0,0),3)
            cv2.line(img,face[idlist[0]],face[idlist[1]],(0,0,255),2)
            cv2.line(img,face[idlist[2]],face[idlist[3]],(0,0,255),2)
    
    # to find the distance b/w the points 
            upDown, _=detector.findDistance(face[idlist[0]],face[idlist[1]])
            leftRight, _=detector.findDistance(face[idlist[2]],face[idlist[3]])
    
    # distace of the ojects 
            cx,cy= (up[0]+down[0])//2 , (up[1]+down[1])//2
            cv2.line(img,(cx,cy),(pos[0]+50,pos[1]+50),(255,0,0),1)
            disMouthObject,_ =detector.findDistance((cx,cy),(pos[0]+50,pos[1]+50))              #_ is used to ignore the second value 
            print(disMouthObject)
            
    
    # lip open or closed 
            ratio= int((upDown / leftRight)*100)
    # print(ratio)
            if ratio>70:
                mouthStatus="OPEN"
            else:
                mouthStatus="CLOSED"
            cv2.putText(img,mouthStatus,(50,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),3) 
    
            if disMouthObject<100 and ratio>70:
                if isEatable:
                    currentObjects=resetObject() 
                    count+=1
                else:
                    gameOver=True
        cv2.putText(img,str(count),(1100,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(255,0,0),4) 
    else:
        cv2.putText(img,"GAME OVER ",(300,400),cv2.FONT_HERSHEY_PLAIN,7,(255,0,0),10) 
        
    cv2.putText(img,"TO QUIT GAME PRESS - q ",(50,650),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4) 
    cv2.putText(img,"TO RESTART GAME PRESS - r ",(50,620),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),4) 
             

    cv2.imshow("Image",img)
    #Waits for 1 millisecond for a key press
    key=cv2.waitKey(1)
    if key == ord('r'):
        resetObject()
        gameOver = False
        count = 0
        currentObjects = eatables[random.randint(0, 3)]
        isEatable = True
    
    # Add key 'q' to quit the game
    if key == ord('q'):
        break

   
     
  
