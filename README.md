# Real-Time-Surveillance-Using-Security-Camera

Dependencies:
1.	Python 3
2.	OpenCV
3.	NumPy
4.	face_recognition
5.	imutils
6.	sklearn
7.	mysql
For local server we have used xampp server.
 
First, we have created a table named picturelog. It will have 4 attributes. Attributes are given below:
1.	ID: This attribute will be an integer type. It must be auto increment and primary key. ID represent the unique number of the face images.
2.	ImagePath: This attribute will be a string type. ImagePath represent the path of the saved face images.
3.	Enter_Time: This attribute will be a string type. Enter_Time represent the entering time of the persons.
4.	Exit_Time: This attribute will also be a string type. Exit_Time represent the exit time of the persons.

How it works:
1.	First, we run “facetrack.py”file to capture the faces of the person using the camera. It will create the “log.txt” file which contains the capturing time of images and save the face images in –dataset and –Face folder. 
2.	Then we run “encode_faces.py” file to create the “encodings.pickle” file of the saved images.
3.	Then we run cluster_faces.py file to cluster the images based on “encodings.pickle” files. This step returns the entering time and exit time of the persons and save this data in our database table which is named “picturelog”.
4.	For face search we run the “app.py” file. It will work on “localhost:5000/hello” address. It returns the html page which contains the upload function for face search. Then upload the images for results. If the picture is found on the database, it will show the log time otherwise it will show not found.
5.	After encodings and clustering delete the images from the –dataset folder.
