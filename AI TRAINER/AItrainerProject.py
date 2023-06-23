import cv2
import numpy as np
import time
import Posemodule as pm
cap=cv2.VideoCapture("EXER.mp4")
import pandas as pd
#cap=cv2.VideoCapture(0)
detector=pm.poseDetector()
count=0
dir=0#we have 2 direction..if dir=0 it means going up and dir=1 =going down so we consider a full curve if it does both of these..full up to dowwn
pTime=0
while True:
    success,img=cap.read()
    img=cv2.resize(img,(1280,720))#jodi video screen size er theke bere jay ba onek kom then we can set our height width of video through this
    # img=cv2.imread("Angledtectionimg.png")#here i have read this image to detect the anglr..
    img=detector.findPose(img,False)#it will detect the image and return the image so i have stored the image..and as we make draw as falsee so it dont show the red point..
    lmlist=detector.findPosition(img,False)#ager pose module e findposition method ta k call korlam jeta amar land mark dey...aar jeta 2 to parameter ney..1.image ta 2.draw korbo kina ..as we dont need to draw here so we made it false..so eta mainly lmlist er modhye land mark gulo store kore debe...
    #print(lmlist)
    if len(lmlist)!=0:
        # #right arm
        # angle=detector.findAngle(img,12,14,16)#eta  ekhon amader dewa 12=p1,14=p2,16=p3 ei 3 te poiner cordinate anujayi select holo..
        # per=np.interp(angle,(25,150),(0,100))#here amra ekta angle er range diyechi 25 theke 150 cover korle
        # print(angle,per)
        
        
        #LEFT arm
         angle=detector.findAngle(img,11,13,15)
         per=np.interp(angle,(230,300),(0,100))#for video
         #per=np.interp(angle,(30,150),(0,100))#here amra ekta angle er range diyechi 25 theke 150 cover korle PERCENTAGE O-->100 HBE...#for real time..
         #print(angle,per)
         bar=np.interp(angle,(230,300),(650,100))
         #bar=np.interp(angle,(25,150),(650,100))
         color=(255,0,255)
         #CHECK DUMBLE CURLS
         if per==100:
             color=(0,255,0)
             if dir==0:#ei conditionta  satify hoche bbcz by default ami prothome age dir=0 kore eschi..
                 count+=0.5#as amake total ekbar up then ekbar down duto  move fully korle tobei count 1 hbe...so  ekhane per100 er por dir ==0 mane  ekbar fully up so 0.5 holo
                 dir=1#the reason behind this os dir=0 ta age theke satisfy korachilo tai if dir==0 ta satisfy hoye gelo but er por next dir=1 down condition ta satisfy korar jonno ekhane dir=1 kore dilam..
         if per==0:
             color=(0,0,255)
             if dir==1:#age dir=0 er end e dir=1 kore diyechilam..
                 count+=0.5#now ekhane baki down curl ta holo then dir==1 satisfied bcz ami up er time i sese dir=1 initialize kore diyechi...so it obviously satsfy the condition
                 dir=0#porer bar abar jate dir=0 ta satiffy hoy thats why..
         print(count) 
         # Draw bar
         cv2.rectangle(img,(1100,100),(1175,650),color,4)
         cv2.rectangle(img,(1100,int(bar)),(1175,650),color,cv2.FILLED)
         cv2.putText(img,f'{int(per)} %',(1100,75),cv2.FONT_HERSHEY_PLAIN,4,color,4)
         
         #Draw curl count
         cv2.rectangle(img,(0,450),(350,720),(155,255,0),cv2.FILLED)
         cv2.putText(img,str(int(count)),(45,670),cv2.FONT_HERSHEY_PLAIN,15,(255,0,0),20)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
    emp={'x CORDINATE':lmlist[0],
        'y CORDINATE':lmlist[1],
        'z CORDINATE':lmlist[2]}
    df=pd.DataFrame(emp,columns=['x CORDINATE','y CORDINATE','z CORDINATE'])
    print("Dislay")
    print(df)
    df.to_csv ("F:\\DESKTOP\\OPENCV\\FOLDER MODULE\\Legxercis.csv")
    df=pd.read_csv("F:\\DESKTOP\\OPENCV\\FOLDER MODULE\\Legxercis.csv")
    print(df)