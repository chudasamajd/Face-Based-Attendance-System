import cv2,os,urllib.request
import numpy as np
from django.conf import settings
import pandas as pd
import time
import datetime

class VideoCameraTest(object):
	def __init__(self):
		#self.video = cv2.VideoCapture(0)
		self.now = time.time()
		self.future = self.now + 20
		self.recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
		try:
			self.recognizer.read("TrainingImageLabel\Trainner.yml")
		except:
			print('Model not found,Please train model')

		self.harcascadePath = "haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(self.harcascadePath)
		self.df = pd.read_csv("StudentDetails.csv")
		self.cam = cv2.VideoCapture(0)
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.col_names = ['ID', 'Name', 'Date', 'Time']
		self.attendance = pd.DataFrame(columns=self.col_names)

	def __del__(self):
		self.cam.release()

	def get_frame(self):
		ret, im = self.cam.read()
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		faces = self.faceCascade.detectMultiScale(gray, 1.2, 5)
		for (x, y, w, h) in faces:
			global Id

			Id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
			if (conf < 70):
				print(conf)
				ts = time.time()
				date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
				timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
				aa = self.df.loc[self.df['ID'] == Id]['NAME'].values
				print(aa)
				# global tt
				# tt = str(Id) + "-" + aa
				# En = '15624031' + str(Id)
				self.attendance.loc[len(self.attendance)] = [Id, aa, date, timeStamp]
				cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
				cv2.putText(im, str(Id), (x + h, y), self.font, 1, (255, 255, 0,), 4)

			else:
				Id = 'Unknown'
				tt = str(Id)
				cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
				cv2.putText(im, str(tt), (x + h, y), self.font, 1, (0, 25, 255), 4)
		# if time.time() > self.future:
		# 	break

		attendance = self.attendance.drop_duplicates(['ID'], keep='first')
		#cv2.imshow('Filling attedance..', im)
		#key = cv2.waitKey(30) & 0xff
		# if key == 27:
		# 	break


		frame_flip = cv2.flip(im,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()
