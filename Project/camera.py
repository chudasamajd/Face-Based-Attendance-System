import cv2,os,urllib.request
import numpy as np
from django.conf import settings
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect,request,response
from django.shortcuts import render,redirect
from django.template.response import TemplateResponse
from . import views
import time
import pandas as pd
import datetime

face_detection_videocam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'haarcascade_frontalface_default.xml'))
face_detection_webcam = cv2.CascadeClassifier(os.path.join(
			settings.BASE_DIR,'haarcascade_frontalface_default.xml'))

class VideoCamera(object):
	def __init__(self):
		#self.video = cv2.VideoCapture(0)
		self.flag = 1
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
		success, image = self.cam.read()

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		file = cv2.CascadeClassifier('D:\\Python Projects\\SoloLearn\\ff.xml')
		try:
			faces = file.detectMultiScale(gray,1.3,5)

			for x,y,w,h in faces:
				#cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				global Id

				Id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
				if (conf < 70):
					print(conf)
					ts = time.time()
					date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
					timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
					aa = self.df.loc[self.df['ID'] == Id]['FIRST_NAME'].values
					print(aa)
					# global tt
					# tt = str(Id) + "-" + aa
					# En = '15624031' + str(Id)
					self.attendance.loc[len(self.attendance)] = [Id, aa, date, timeStamp]
					cv2.rectangle(image, (x, y), (x + w, y + h), (0, 260, 0), 7)
					cv2.putText(image, str(Id), (x + h, y), self.font, 1, (255, 255, 0,), 4)

					if self.flag == 1:
						self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
						ts = time.time()
						date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
						timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
						Hour, Minute, Second = timeStamp.split(":")
						fileName = "Attendance/" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
						self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
						print(self.attendance)
						self.attendance.to_csv(fileName, index=False)
						self.flag = 0
				else:
					Id = 'Unknown'
					tt = str(Id)
					cv2.rectangle(image, (x, y), (x + w, y + h), (0, 25, 255), 7)
					cv2.putText(image, str(tt), (x + h, y), self.font, 1, (0, 25, 255), 4)
					# if self.flag == 1:
					# 	self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
					# 	ts = time.time()
					# 	date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
					# 	timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
					# 	Hour, Minute, Second = timeStamp.split(":")
					# 	fileName = "Attendance/" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
					# 	self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
					# 	print(self.attendance)
					# 	self.attendance.to_csv(fileName, index=False)
					# 	self.flag = 0

		except Exception as e:
			print(e)

		#frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

class VideoCameraT(object):
	def __init__(self):
		#self.video = cv2.VideoCapture(0)
		self.flag = 1
		self.now = time.time()
		self.future = self.now + 20
		self.recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
		try:
			self.recognizer.read("TrainingImageTeacherLabel\Trainner.yml")
		except:
			print('Model not found,Please train model')

		self.harcascadePath = "haarcascade_frontalface_default.xml"
		self.faceCascade = cv2.CascadeClassifier(self.harcascadePath)
		self.df = pd.read_csv("TeacherDetails.csv")
		self.cam = cv2.VideoCapture(0)
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.col_names = ['ID', 'Name', 'Date', 'Time']
		self.attendance = pd.DataFrame(columns=self.col_names)

	def __del__(self):
		self.cam.release()


	def get_frame(self):
		success, image = self.cam.read()

		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		file = cv2.CascadeClassifier('D:\\Python Projects\\SoloLearn\\ff.xml')
		try:
			faces = file.detectMultiScale(gray,1.3,5)

			for x,y,w,h in faces:
				#cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				global Id

				Id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
				if (conf < 70):
					print(conf)
					ts = time.time()
					date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
					timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
					aa = self.df.loc[self.df['ID'] == Id]['FIRST_NAME'].values
					print(aa)
					# global tt
					# tt = str(Id) + "-" + aa
					# En = '15624031' + str(Id)
					self.attendance.loc[len(self.attendance)] = [Id, aa, date, timeStamp]
					cv2.rectangle(image, (x, y), (x + w, y + h), (0, 260, 0), 7)
					cv2.putText(image, str(Id), (x + h, y), self.font, 1, (255, 255, 0,), 4)

					if self.flag == 1:
						self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
						ts = time.time()
						date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
						timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
						Hour, Minute, Second = timeStamp.split(":")
						fileName = "AttendanceTeacher/" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
						self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
						print(self.attendance)
						self.attendance.to_csv(fileName, index=False)
						self.flag = 0
				else:
					Id = 'Unknown'
					tt = str(Id)
					cv2.rectangle(image, (x, y), (x + w, y + h), (0, 25, 255), 7)
					cv2.putText(image, str(tt), (x + h, y), self.font, 1, (0, 25, 255), 4)
					# if self.flag == 1:
					# 	self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
					# 	ts = time.time()
					# 	date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
					# 	timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
					# 	Hour, Minute, Second = timeStamp.split(":")
					# 	fileName = "AttendanceTeacher/" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
					# 	self.attendance = self.attendance.drop_duplicates(['ID'], keep='first')
					# 	print(self.attendance)
					# 	self.attendance.to_csv(fileName, index=False)
					# 	self.flag = 0

		except Exception as e:
			print(e)

		#frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()


class VideoCamera2(object):
	def __init__(self,sid):
		self.sampleNum = 0
		self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		self.sid = sid

	def __del__(self):
		self.video.release()

	def get_frame(self):
		try:
			success, image = self.video.read()

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			file = cv2.CascadeClassifier('D:\\Python Projects\\SoloLearn\\ff.xml')

			faces = file.detectMultiScale(gray,1.3,5)

			for x,y,w,h in faces:
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				self.sampleNum = self.sampleNum + 1
				# saving the captured face in the dataset folder
				if self.sampleNum < 100:
					cv2.imwrite("TrainingImage/test."+str(self.sid)+"." + str(self.sampleNum) + ".jpg",
							gray[y:y + h, x:x + w])
				if self.sampleNum == 100:
					self.current_num()



			frame_flip = cv2.flip(image,1)
			ret, jpeg = cv2.imencode('.jpg', frame_flip)

			return jpeg.tobytes()
		except Exception as e:
			pass

	def current_num(self):
		print(self.sampleNum)
		if self.sampleNum == 100:
			cv2.destroyAllWindows()
			self.video.release()
			#return HttpResponse('hi')
		#return redirect("template/admin.html")


class VideoCamera3(object):
	def __init__(self,sid):
		self.sampleNum = 0
		self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
		self.sid = sid

	def __del__(self):
		self.video.release()

	def get_frame(self):
		try:
			success, image = self.video.read()

			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			file = cv2.CascadeClassifier('D:\\Python Projects\\SoloLearn\\ff.xml')

			faces = file.detectMultiScale(gray,1.3,5)

			for x,y,w,h in faces:
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				self.sampleNum = self.sampleNum + 1
				# saving the captured face in the dataset folder
				if self.sampleNum < 100:
					cv2.imwrite("TrainingImageTeacher/test."+str(self.sid)+"." + str(self.sampleNum) + ".jpg",
							gray[y:y + h, x:x + w])
				if self.sampleNum == 100:
					self.current_num()



			frame_flip = cv2.flip(image,1)
			ret, jpeg = cv2.imencode('.jpg', frame_flip)

			return jpeg.tobytes()
		except Exception as e:
			pass

	def current_num(self):
		print(self.sampleNum)
		if self.sampleNum == 100:
			cv2.destroyAllWindows()
			self.video.release()
			#return HttpResponse('hi')
		#return redirect("template/admin.html")

