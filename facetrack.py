import numpy as np
import cv2
import datetime


file = open("log.txt","w")
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('people.mp4')
samplenumber = 0

while 1:
	ret, img = cap.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)

	for (x,y,w,h) in faces:
		samplenumber = samplenumber + 1
		time = datetime.datetime.now().strftime("%A %d %B %Y %I %M %S%p")
		
		file.write(str(samplenumber)+"."+str(time)+"\n")
		#path = "D:\faceClustering\simple-object-tracking\dataset/User."
		#path += str(samplenumber) + ".jpg"
		cv2.imwrite("dataset/User."+str(samplenumber)+".jpg",img[y:y+h, x:x+w])
		cv2.imwrite("Face/User."+str(samplenumber)+".jpg",img[y:y+h, x:x+w])
		
		#sql_insert_query =  INSERT INTO 'picturerecord' ('ID', 'ImagePath', 'Enter_Time', 'Exit_Time') VALUES (samplenumber,path)
		
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	

	cv2.putText(img, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, img.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	cv2.imshow('img',img)
	
	if cv2.waitKey(1) == ord("q"):
		break

file.close()
cap.release()
cv2.destroyAllWindows()
