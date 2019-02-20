from flask import Flask, render_template, request, flash, redirect
import os
import face_recognition
import argparse
import cv2
from numpy import array

import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="timelog")

mycursor = mydb.cursor()

mycursor.execute("SELECT ImagePath, Enter_Time, Exit_Time FROM demo2")

myresult = mycursor.fetchall()
L = list()
for x in myresult:
    L.append(x)

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detection-method", type=str, default="cnn",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['jpg']


@app.route("/hello")
def hello():
    return render_template("index2.html")


@app.route("/submission", methods=['POST'])
def submission():
    if request.method == 'POST':
        # f = request.files['my_image']
        # f.save('C:\\Users\\Mong Ting\\PycharmProjects\\untitled3')
        # return redirect()
        # check if the post request has the file part
        if 'my_image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['my_image']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'known.jpg'
            file.save(os.path.join('.\\static', filename))

            known_image = face_recognition.load_image_file(
                "C:\\Users\\Mong Ting\\PycharmProjects\\untitled3\\static\\known.jpg")
            rgb1 = cv2.cvtColor(known_image, cv2.COLOR_BGR2RGB)
            boxes1 = face_recognition.face_locations(rgb1, model=args["detection_method"])
            encodings1 = face_recognition.face_encodings(rgb1, boxes1)
            en1 = array(encodings1)[0]
            ck = 0
            resultsss = ""
            startlist = []
            endlist = []
            for i in L:
                unknown_image = face_recognition.load_image_file(i[0])
                rgb2 = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
                boxes2 = face_recognition.face_locations(rgb2, model=args["detection_method"])
                encodings2 = face_recognition.face_encodings(rgb2, boxes2)
                en2 = array(encodings2)[0]
                results = face_recognition.compare_faces([en1], en2)
                if str(results[0]) == "True":
                    ck = 1
                    filepath = i[0]
                    enter_time = i[1]
                    exit_time = i[2]
                    startlist.append(enter_time)
                    endlist.append(exit_time)
                    resultsss += '\n' + i[0] + "EnterTime: " + i[1] + '\n' + "ExitTime: " + i[2] + '\n'

                else:
                    print("NOt OK")

            # print(resultsss)
            print(len(startlist))

            if ck == 1:
                return render_template("index1.html", user_image="static\\known.jpg", enter_time=startlist,
                                       exit_time=endlist)
            else:
                return "<h2>Not Found!!! </h2>"

        return '''
            DONE
    '''


if __name__ == '__main__':
    app.run(debug=True)
