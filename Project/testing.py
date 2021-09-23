import cv2
import pandas as pd
import time
import datetime

now = time.time()  ###For calculate seconds of video
future = now + 20
recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
try:
    recognizer.read("../TrainingImageLabel\Trainner.yml")
except:
    print('Model not found,Please train model')

harcascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath)
df = pd.read_csv("../StudentDetails.csv")
cam = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
col_names = ['ID', 'Name', 'Date', 'Time']
attendance = pd.DataFrame(columns=col_names)
while True:
    ret, im = cam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
    for (x, y, w, h) in faces:
        global Id

        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        if (conf <70):
            print(conf)
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            aa = df.loc[df['ID'] == Id]['NAME'].values
            print(aa)
            # global tt
            #tt = str(Id) + "-" + aa
            # En = '15624031' + str(Id)
            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
            cv2.putText(im, str(Id), (x + h, y), font, 1, (255, 255, 0,), 4)

        else:
            Id = 'Unknown'
            tt = str(Id)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
    if time.time() > future:
        break

    attendance = attendance.drop_duplicates(['ID'], keep='first')
    cv2.imshow('Filling attedance..', im)
    key = cv2.waitKey(30) & 0xff
    if key == 27:
        break

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour, Minute, Second = timeStamp.split(":")
fileName = "../Attendance/" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
attendance = attendance.drop_duplicates(['ID'], keep='first')
print(attendance)
attendance.to_csv(fileName, index=False)