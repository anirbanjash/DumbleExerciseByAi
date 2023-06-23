import imp
from sre_constants import SUCCESS
import time
import os
import math
import  cv2 #it is use for image processing
import mediapipe as mp #it is a frame work that ewill allow us to get our pose estimation
# now we have to read our video..
class poseDetector():
    def __init__(self,mode=False,model_complexity=1,upBody=False,smooth=True,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.model_complexity=model_complexity
        self.upBody=upBody
        self.smooth=smooth
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.model_complexity,self.upBody,self.smooth,self.detectionCon,self.trackCon)
        
    def findPose(self,img,draw=True):#this draw=true will ask that do u want to draw or not..
        
    
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(imgRGB)#Now after conversion we have simply going to send our image to our model..
        # print(self.results.pose_landmarks)#through this we will get our landmarks in  xy z and visibility  ..
        #now we will check it is detected or not...
        
        if self.results.pose_landmarks:#etaar mane result of landmarks avaiable hole draw korno..
                if draw:
                     self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return img
                
    def findPosition(self,img,draw=True):    
        self.lmList=[]#i add here self now it is a part of that object..       
        if self.results.pose_landmarks: #it means if the resulrs are available then we to start the loop..       
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                # print(id,lm)#now protyek red point means land mark er jonno loop cholbe aar protyek ta  red point landmark er index id hisebe  store hbe and it  will show..with x y and visibility..
            #enumerate will give us loop count...
                #what  ever we got from print(id,km)==>lm's x y .. are in ratio thats why all values are in decimel..
                #so now to get the original pixel value we have to do:
                cx,cy=int( lm.x*w),int(lm.y*h);
                self.lmList.append([id,cx,cy])#list er vetor id cx cy  value append korlam for 32 id 32 x and y condinates we will get..
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)#this will over lay previous red small points to big and blue  points ,cx cy are our cordinates,10 is radius of circle,colour in  bgr
        return self.lmList#it will return our 33 (0 to 32) points cordinates...by storing in to the list..and jotobar sei point gulo image e move korbe totobar tar screen e new new cordinate o dekhabw..
    def findAngle(self,img,p1,p2,p3,draw=True):#here for measurig the angle we create a mthod..and here p1 ,p2,p3 is basically index of red points or landmarks..by using this we get the angle and here as draw korbo so draw=true dilam
        #GET THE LANDMARKS
        x1,y1=self.lmList[p1][1:]
        x2,y2=self.lmList[p2][1:]
        x3,y3=self.lmList[p3][1:]
        #here basically wahat happend amra jani lmlist e amar points der index,x corddinate,y cordinate ei order e store thake...now for calculating angle we need pony x and y cordinates of 3 points p1 p2 p2=>for that   lmlist er p1 point er jonno mane p1 index er jonno ami traversal koralam array of p1 position er arrayr from index 1 tahole automatic 0 index e thaka index of p1 bad diye only x and y cordinated pabo.seta x1  e x cordinate aar y1 e y cordinate store hbe...same for p2 and p3 
        #CALCULATE THE ANGLE
        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        #print(angle)#so it will show the angle..
        if angle<0:
            angle+=360#kono negetive angle ele setake positive korar jonno
        #DRAW
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)#joining x1 and x2 through a green line
            cv2.line(img,(x3,y3),(x2,y2),(0,255,0),3)#joining x2 and x3 through a green line
            cv2.circle(img,(x1,y1),8,(0,0,255),cv2.FILLED)#etay filler mane circle ta filled thakbe
            cv2.circle(img,(x1,y1),15,(255,0,0),2) #etay filled nai mane just circle thakbe vetor ta faka
            cv2.circle(img,(x2,y2),8,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,0),2)
            cv2.circle(img,(x3,y3),8,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x3,y3),15,(255,0,0),2)
            cv2.putText(img,f'{str(int(angle))} Degree',(x2-50,y2+40),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)#here img nilam, then as angle ta int form e  ache otake string e convert korlam.,. then kon jaygatay actually ami show korabo angle ta set adilam x2 means middle point er x cordinate  theke 50 less and  y cordinate thek50 besi point e.., then font dilam aketa,then scale,then colour,then thick ness..
            return angle 
            
def main():
     folderpath="Posevideos"
     myList=os.listdir(folderpath)
     print(myList)
     cap=cv2.VideoCapture(f'{folderpath}/{myList[1]}')
      
     #here i have given 0 for may laptop webcam...
     pTime=0#???
     detector=poseDetector()
     while True:
        SUCCESS, img=cap.read()# ja image capture hbe seta cap e ache then seta read hoche
        img=detector.findPose(img)
        lmList=detector.findPosition(img,draw=False)
        if len(lmList)!=0:
            cv2.circle(img,(lmList[14][1],lmList[14][2]),10,(255,0,0),cv2.FILLED)
            print(lmList[10])
        cTime=time.time()
        fps=1/(cTime-pTime)#cTime=current time pTime=previous time
        pTime=cTime#??/
        cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)#eta fps print er jonno
        #KOTHAY ANKBO ??=> img te ,,ki ankgo ==>fps (ami only text pari mane only string so typecast korlam),kothay ankbo??=> co ordinates of frame,style,3=font size ,255,43,234 BGR. e
        cv2.imshow("Image",img)## jeta capture hoyeche ota show kore dao 
        cv2.waitKey(1)##you have to wait ,er main kaj ,aager j image ta esche ota k stay koray ,ei wait key command ta..erom sec sec e age img ta rakhe ba wait koray.and ddelay koray 1 milliseccond  
if __name__=="__main__":#The thing what it does actually if we run this function with itself(means with his name posemodule) it  will call the main function and if we call another function it willl run this main part..
    main()