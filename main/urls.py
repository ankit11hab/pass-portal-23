from django.urls import path
from . import views

urlpatterns = [
    path('', views.comingsoon, name="comingsoon"),
    path('h7564', views.home, name="home"),
    path('otp23/', views.otp, name="send_otp"),
    path('confirm12/', views.confirm, name="confirm"),
    path('submit43/', views.send_otp, name='otp'),
    path('verify21/', views.verify, name='verify'),
    path('verify32/submit/', views.verify_otp, name='verify_otp'),
    path('register12/', views.register, name='register'),
    path('register12/submit/', views.SaveData, name='SaveData'),
    path('managebooking/', views.manangebooking, name='managebooking'),
    path('manage_booking/', views.manage_booking_page, name='manage_booking'),
    path('verify_otp/', views.verifiy_otp_manage_booking, name='verifiy_otp_manage_booking'),
] 
