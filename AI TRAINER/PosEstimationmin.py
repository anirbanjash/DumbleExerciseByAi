from sre_constants import SUCCESS
import time
import  cv2 #it is use for image processing
import mediapipe as mp #it is a frame work that ewill allow us to get our pose estimation
# now we have to read our video..
mpDraw=mp.solutions.drawing_utils
mpPose=mp.solutions.pose
pose=mpPose.Pose ()
cap=cv2.VideoCapture(0)#here i have given 0 for may laptop webcam...
pTime=0#???
while True:
    SUCCESS,img=cap.read()# ja image capture hbe seta cap e ache then seta read hoche
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=pose.process(imgRGB)#Now after conversion we have simply going to send our image to our model..
    # print(results.pose_landmarks)#through this we will get our landmarks in  xy z and visibility  ..
    #now we will check it is detected or not...
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS)#it will draw our landmarks...in red colour..
        #here pose_landmarks will create the red point..and POSE_CONNECTION WILL CREATE THE CONNECTIONS BETWEEN POINTS..
        #NOW IN TERMINAL LANDMARKS IS SHOWING..NOISSUES BUT WHICH LAANK MARK IS FOR WHICH WE DON’T KNOW..THERE ARE 32 POINTS…SO WE HAVE TO IDENTIFY WHICH POINT HAVE WHICH LANDMARKS..FOR THAT:
        for id,lm in enumerate(results.pose_landmarks.landmark):
            h,w,c=img.shape
            print(id,lm)#now protyek red point means land mark er jonno loop cholbe aar protyek ta  red point landmark er index id hisebe  store hbe and it  will show..with x y and visibility..
        #enumerate will give us loop count...
            #what  ever we got from print(id,km)==>lm's x y .. are in ratio thats why all values are in decimel..
            #so now to get the original pixel value we have to do:
            cx,cy=int( lm.x*w),int(lm.y*h);
            cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED)#this will over lay previous red small points to big and blue  points ,cx cy are our cordinates,10 is radius of circle,colour in  bgr
    cTime=time.time()
    fps=1/(cTime-pTime)#cTime=current time pTime=previous time
    pTime=cTime#??/
    cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    #KOTHAY ANKBO ??=> img te ,,ki ankgo ==>fps (ami only text pari mane only string so typecast korlam),kothay ankbo??=> co ordinates of frame,style,3=font size ,255,43,234 BGR.
    cv2.imshow("Image",img)## jeta capture hoyeche ota show kore dao 
    cv2.waitKey(1)##you have to wait ,er main kaj ,aager j image ta esche ota k stay koray ,ei wait key command ta..erom sec sec e age img ta rakhe ba wait koray.and ddelay koray 1 milliseccond

