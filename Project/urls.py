"""Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('window',views.window,name='window'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('admin',views.admin),
    path('admin_login',views.admin_login),
    path('admin_registration',views.admin_registration),
    path('admin_registration_data',views.admin_registration_data),
    path('admin_login_data',views.admin_login_data),
    path('admin_home',views.admin_home),
    path('teacher',views.teacher),
    path('take_sample',views.take_sample),
    path('take_sample2',views.take_sample2),
    path('video_feed2', views.video_feed2, name='video_feed2'),
    path('video_feed3', views.video_feed3, name='video_feed3'),
    path('std_registration',views.std_registration),
    path('std_registration_data',views.std_registration_data),
    path('adminLogin',views.adminLogin),
    path('adminLoginData',views.adminLoginData),
    path('trainModel',views.trainModel),
    path('trainModel2',views.trainModel2),
    path('test',views.testing),
    path('test2',views.testing2),
    path('video_feed_test', views.video_feed_test, name='video_feed_test'),
    path('video_feed_test2', views.video_feed_test2, name='video_feed_test2'),
    path('std_detail',views.std_detail),
    path('teacher_detail',views.teacher_detail),
    path('std_attendance_detail',views.std_attendance_detail),
    path('teacher_attendance_detail',views.teacher_attendance_detail),
    path('logout',views.logout),
    path('forgot_password',views.forgotPassword),
]
