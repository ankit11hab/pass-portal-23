from django.urls import path
from . import views

urlpatterns = [
    # path('mail', views.generate_qr_code, name='QRcode'),
    path('', views.home, name="home"),
    path('otp', views.otp, name="send_otp"),
    path('confirm/', views.confirm, name="confirm"),
    path('submit/', views.send_otp, name='otp'),
    path('verify/', views.verify, name='verify'),
    path('verify/submit/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('register/submit/', views.SaveData, name='SaveData'),
    path('confirmPayment/',views.confirm_payment, name ='Confirm_Payment'),
] 
