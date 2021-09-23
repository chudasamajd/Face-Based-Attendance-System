from django.http import HttpResponse,HttpRequest,request
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from .camera import VideoCamera,VideoCamera2,VideoCamera3,VideoCameraT
import csv
import pandas as pd
import os
from .training import getImagesAndLabels
import cv2
import numpy as np
from .test import VideoCameraTest
from django.core.mail import send_mail

Id =''
TId = ''
admin_status = 0

def index(HttpRequest):
    return render(HttpRequest,'index.html')

def window(HttpRequest):
    return render(HttpRequest,'window.html')

def gen(camera):
	try:
		while True:
			frame = camera.get_frame()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	except:
		pass
def gen2(camera):
	try:
		while True:
			frame = camera.get_frame()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	except:
		pass


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def admin(HttpRequest):
	global admin_status
	if admin_status == 1:
		return render(HttpRequest,'admin.html')
	else:
		return render(HttpRequest, 'adminLogin.html')


def admin_login(HttpRequest):
	return render(HttpRequest,'admin_login.html')

def admin_registration(HttpRequest):
	global admin_status
	if admin_status == 1:
		return render(HttpRequest,'admin_registration.html')
	else:
		return render(HttpRequest, 'adminLogin.html')


def admin_registration_data(HttpRequest):
	global TId

	stdfirstname = HttpRequest.POST.get('stdfirstname')
	stdlastname = HttpRequest.POST.get('stdlastname')
	stdsurname = HttpRequest.POST.get('stdsurname')
	stddob = HttpRequest.POST.get('stddob')
	stdphone = HttpRequest.POST.get('stdphone')
	stdaddress = HttpRequest.POST.get('stdaddress')
	stdemail = HttpRequest.POST.get('stdemail')

	try:
		imagePaths = [os.path.join('TrainingImageTeacher', f) for f in os.listdir('TrainingImageTeacher')]
		if len(imagePaths) == 0:
			TId = 1
		else:
			for imagePath in imagePaths:
				TId = int(os.path.split(imagePath)[-1].split(".")[1]) + 1
	except:
		TId = 1

	row = [TId, stdfirstname, stdlastname, stdsurname, stddob, stdphone, stdaddress, stdemail]

	with open('TeacherDetails.csv', 'a+') as csvFile:
		writer = csv.writer(csvFile, delimiter=',')
		writer.writerow(row)
		csvFile.close()

	return render(HttpRequest, 'take_sample2.html')

def admin_login_data(HttpRequest):
	username = HttpRequest.POST.get('username')
	password = HttpRequest.POST.get('password')

	data = pd.read_csv('TeacherDetails.csv')
	subsetDataFrame = data[(data['TEACHER_ID'] == int(password)) & (data['NAME'] == username)]
	if len(subsetDataFrame):
		return render(HttpRequest,'teacher.html')
	else:
		return render(HttpRequest,'admin_login.html',{'data':1})

def adminLogin(HttpRequest):
	return render(HttpRequest, 'adminLogin.html')

def adminLoginData(HttpRequest):
	global admin_status
	username = HttpRequest.POST.get('username')
	password = HttpRequest.POST.get('pass')
	if username == 'admin' and password == 'admin':
		admin_status = 1
		return render(HttpRequest, 'admin.html')
	else:
		return render(HttpRequest, 'adminLogin.html', {'data': 1})

def admin_home(HttpRequest):
	global admin_status
	if admin_status==1:
		return render(HttpRequest,'admin_home.html')
	else:
		return render(HttpRequest, 'adminLogin.html')


def teacher(HttpRequest):
	return render(HttpRequest,'teacher.html')

def take_sample(HttpRequest):
	return render(HttpRequest,'take_sample.html')

def take_sample2(HttpRequest):
	return render(HttpRequest,'take_sample2.html')

def video_feed2(request):
	global Id
	return StreamingHttpResponse(gen(VideoCamera2(Id)),
					content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed3(request):
	global TId
	return StreamingHttpResponse(gen2(VideoCamera3(TId)),
					content_type='multipart/x-mixed-replace; boundary=frame')


def std_registration(HttpRequest):
	global admin_status
	if admin_status == 1:
		return render(HttpRequest,'student_registration.html')
	else:
		return render(HttpRequest, 'adminLogin.html')

def std_registration_data(HttpRequest):
	global Id

	stdfirstname = HttpRequest.POST.get('stdfirstname')
	stdlastname = HttpRequest.POST.get('stdlastname')
	stdsurname = HttpRequest.POST.get('stdsurname')
	stdfname = HttpRequest.POST.get('stdfname')
	stddob = HttpRequest.POST.get('stddob')
	stdphone = HttpRequest.POST.get('stdphone')
	stdfatherphone = HttpRequest.POST.get('stdfatherphone')
	stdaddress = HttpRequest.POST.get('stdaddress')
	stdemail = HttpRequest.POST.get('stdemail')

	try:
		imagePaths = [os.path.join('TrainingImage', f) for f in os.listdir('TrainingImage')]
		if len(imagePaths) == 0:
			Id = 1
		else:
			for imagePath in imagePaths:
				Id = int(os.path.split(imagePath)[-1].split(".")[1])+1
	except:
		Id = 1

	row = [Id, stdfirstname, stdlastname, stdsurname, stdfname, stddob, stdphone, stdfatherphone,stdaddress, stdemail]


	with open('StudentDetails.csv', 'a+') as csvFile:
		writer = csv.writer(csvFile, delimiter=',')
		writer.writerow(row)
		csvFile.close()

	return render(HttpRequest,'take_sample.html')

def trainModel(HttpRequest):
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	faces, Ids = getImagesAndLabels('TrainingImage')
	recognizer.train(faces, np.array(Ids))
	recognizer.save('TrainingImageLabel/trainner.yml')
	return render(HttpRequest,'admin.html')

def trainModel2(HttpRequest):
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	faces, Ids = getImagesAndLabels('TrainingImageTeacher')
	recognizer.train(faces, np.array(Ids))
	recognizer.save('TrainingImageTeacherLabel/trainner.yml')
	return render(HttpRequest,'admin.html')

def testing(HttpRequest):
	return render(HttpRequest,'test.html')

def testing2(HttpRequest):
	return render(HttpRequest,'test2.html')

def gen2(camera):
	try:
		while True:
			frame = camera.get_frame()
			yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	except:
		pass

def video_feed_test(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed_test2(request):
	return StreamingHttpResponse(gen(VideoCameraT()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def std_detail(HttpRequest):
	global admin_status
	if admin_status == 1:
		file = pd.read_csv('StudentDetails.csv')
		ids = file['ID']
		fname = file['FIRST_NAME']
		lname = file['LAST_NAME']
		surname = file['SURNAME']
		FATHER_NAME = file['FATHER_NAME']
		DOB = file['DOB']
		PHONE = file['PHONE']
		FPHONE = file['FPHONE']
		ADDRESS = file['ADDRESS']
		EMAIL = file['EMAIL']

		data = zip(ids,fname,lname,surname,FATHER_NAME,DOB,PHONE,FPHONE,ADDRESS,EMAIL)
		return render(HttpRequest,'student_detail.html',{'data':data})
	else:
		return render(HttpRequest, 'adminLogin.html')

def teacher_detail(HttpRequest):
	global admin_status
	if admin_status == 1:
		file = pd.read_csv('TeacherDetails.csv')
		ids = file['ID']
		fname = file['FIRST_NAME']
		lname = file['LAST_NAME']
		surname = file['SURNAME']
		DOB = file['DOB']
		PHONE = file['PHONE']
		ADDRESS = file['ADDRESS']
		EMAIL = file['EMAIL']

		data = zip(ids,fname,lname,surname,DOB,PHONE,ADDRESS,EMAIL)
		return render(HttpRequest,'teacher_detail.html',{'data':data})
	else:
		return render(HttpRequest, 'adminLogin.html')


def std_attendance_detail(HttpRequest):
	global admin_status
	if admin_status == 1:
		imagePaths = [os.path.join('Attendance', f) for f in os.listdir('Attendance')]
		if len(imagePaths) == 0:
			print('Empty')
		else:
			ids = []
			name = []
			dates = []
			result = []
			try:
				for imagePath in imagePaths:
					temp = []
					#Id = int(os.path.split(imagePath)[-1].split(".")[1]) + 1
					file = pd.read_csv(imagePath)
					ids.append(file['ID'][0])
					#print(ids)
					for imagePath2 in imagePaths:

						file2 = pd.read_csv(imagePath2)
						testid = file2['ID'][0]
						if file['ID'][0] == testid:

							#dates.append(int(str(file2['Date'][0]).split("-")[2]))
							d = int(str(file2['Date'][0]).split("-")[2])
							#print('Match :', file['ID'][0], "==", testid,"For Date :",d)
							if d not in temp:
								temp.append(d)
					if [file['ID'][0],temp] not in result:
						result.append([file['ID'][0],temp])
			except:
				pass
			#print(result)
#			data = [[1,[2,3,16]],[2,[2,6]]]
			#nids = []
			#ndates = dict()
			#keys = set(ids)
			#for key in keys:
			#	work(key,data)

				#ndates[key] = items
			#print(ndates)
		return render(HttpRequest,'student_attendance_detail.html',{'data':result,'days':range(1,32)})
	else:
		return render(HttpRequest, 'adminLogin.html')

def teacher_attendance_detail(HttpRequest):
	global admin_status
	if admin_status == 1:
		imagePaths = [os.path.join('AttendanceTeacher', f) for f in os.listdir('AttendanceTeacher')]
		if len(imagePaths) == 0:
			print('Empty')
		else:
			ids = []
			name = []
			dates = []
			result = []
			try:
				for imagePath in imagePaths:
					temp = []
					#Id = int(os.path.split(imagePath)[-1].split(".")[1]) + 1
					file = pd.read_csv(imagePath)
					ids.append(file['ID'][0])
					#print(ids)
					for imagePath2 in imagePaths:

						file2 = pd.read_csv(imagePath2)
						testid = file2['ID'][0]
						if file['ID'][0] == testid:

							#dates.append(int(str(file2['Date'][0]).split("-")[2]))
							d = int(str(file2['Date'][0]).split("-")[2])
							#print('Match :', file['ID'][0], "==", testid,"For Date :",d)
							if d not in temp:
								temp.append(d)
					if [file['ID'][0],temp] not in result:
						result.append([file['ID'][0],temp])
			except:
				pass
			#print(result)
#			data = [[1,[2,3,16]],[2,[2,6]]]
			#nids = []
			#ndates = dict()
			#keys = set(ids)
			#for key in keys:
			#	work(key,data)

				#ndates[key] = items
			#print(ndates)
		return render(HttpRequest,'teacher_attendance_detail.html',{'data':result,'days':range(1,32)})
	else:
		return render(HttpRequest, 'adminLogin.html')



def work(key,data):
	items = []
	for i, j, k in data:
		if i == key:
			print(key,"=",k)
			items.append(k)
	print(key,items)

def logout(HttpRequest):
	global admin_status
	admin_status = 0
	return render(HttpRequest,'adminLogin.html')

def forgotPassword(HttpRequest):
	return render(HttpRequest,'sent_mail.html')