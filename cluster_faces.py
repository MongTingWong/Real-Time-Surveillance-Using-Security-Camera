# USAGE
# python cluster_faces.py --encodings encodings.pickle

# import the necessary packages
from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import face_recognition
import mysql.connector

connection = mysql.connector.connect(host='localhost',database = 'timelog', user='root',password='')
mycursor = connection.cursor()


file=open("log.txt","r")

log_dict={}

for i in file.readlines():
	id=""
	td=""
	d=0
	for j in range(len(i)):
		if(i[j]!='.'):
			id+=i[j]
			d+=1
		else:
			d+=1
			break
	
	for j in range(d,len(i)):
		td+=i[j]
		
	log_dict.update({int(id):td})	
		
#print(log_dict)
		
ck = 0
ck1 = 0
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-j", "--jobs", type=int, default=-1,
	help="# of parallel jobs to run (-1 will use all CPUs)")
args = vars(ap.parse_args())

# load the serialized face encodings + bounding box locations from
# disk, then extract the set of encodings to so we can cluster on
# them
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
data = np.array(data)
encodings = [d["encoding"] for d in data]

# cluster the embeddings
print("[INFO] clustering...")
clt = DBSCAN(metric="euclidean", n_jobs=args["jobs"])
clt.fit(encodings)

# determine the total number of unique faces found in the dataset
labelIDs = np.unique(clt.labels_)
numUniqueFaces = len(np.where(labelIDs > -1)[0])
print("[INFO] # unique faces: {}".format(numUniqueFaces))

# loop over the unique face integers
samplenumber = 0
for labelID in labelIDs:
	
	print("[INFO] faces for face ID: {}".format(labelID))
	idxs = np.where(clt.labels_ == labelID)[0]
	idxs = np.random.choice(idxs, size=min(25, len(idxs)),
		replace=False)

	
	faces = []
	facess= []
	numberlist = []
	samplenumber = samplenumber + 1
	ck1 = 0

	for i in idxs:
		
		image = cv2.imread(data[i]["imagePath"])
		imagenumber = data[i]["imagePath"]
		s = ''.join(x for x in imagenumber if x.isdigit())
		numberlist.append(int(s))
		
		(top, right, bottom, left) = data[i]["loc"]
		face = image[top:bottom, left:right]
		
		faces.append(face)
		
		if(ck1==0):
			#C:\Users\Mong Ting\PycharmProjects\untitled3\simple-object-tracking
			path = "C:\\Users" +"\\Mong Ting\\PycharmProjects\\untitled3\\"+"simple-object-tracking\\"
			path += data[i]["imagePath"]
			path = path.replace("dataset","Face")
			print(path)
			facess.append(face)
		ck1= 1
		
	
	numberlist.sort()
	print("Face ID : " + str(labelID))
	
	print("Entering Time : "+log_dict[numberlist[0]])
	print("Exit Time : "+log_dict[numberlist[len(numberlist)-1]])
	sql_insert_query =  " INSERT INTO picturelog ( ID,ImagePath, Enter_Time, Exit_Time) VALUES (%s,%s,%s,%s)"
	val = (samplenumber,path,log_dict[numberlist[0]],log_dict[numberlist[len(numberlist)-1]])
	
	result = mycursor.execute(sql_insert_query,val)
	connection.commit()
	ck1 = 0
	'''for i in faces:
		if ck==0:
			cv2.imwrite("Mong.jpg",i)
			known_image = face_recognition.load_image_file("Mong.jpg")
			unknown_image = face_recognition.load_image_file("ONE.jpg")
			biden_encoding = face_recognition.face_encodings(known_image)[0]
			unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

			results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
			print("Same Picture hole true or false == " + str(results))
			ck = 1
			
	ck = 0'''
	# create a montage using 96x96 "tiles" with 5 rows and 5 columns
	montage = build_montages(faces, (96, 96), (5, 5))[0]
	
	# show the output montage
	title = "Face ID #{}".format(labelID)
	title = "Unknown Faces" if labelID == -1 else title
	cv2.imshow(title, montage)
	cv2.waitKey(0)