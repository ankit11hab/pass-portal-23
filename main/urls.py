from django.urls import path
from . import views

urlpatterns = [
    path('gbvh4457d', views.comingsoon, name="comingsoon"),
    path('', views.home, name="home"),
    path('otp/', views.otp, name="send_otp"),
    path('confirm/', views.confirm, name="confirm"),
    path('submit/', views.send_otp, name='otp'),
    path('verify/', views.verify, name='verify'),
    path('verify/submit/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('register/submit/', views.SaveData, name='SaveData'),
    path('managebooking/', views.manangebooking, name='managebooking'),
    path('manage_booking/', views.manage_booking_page, name='manage_booking'),
    path('verify_otp/', views.verifiy_otp_manage_booking, name='verifiy_otp_manage_booking'),
    path('backup/users',views.backupData_users),
    path('backup/verifiedusers',views.backupData_verified_users),
    path('backup/transactions',views.backupData_transactions),
    path('dletesfdsdfar32',views.delete_kardega),
    path('w2kmfu7rh',views.all_verified_users),
] 
