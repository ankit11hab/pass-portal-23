from django.urls import path
from . import views

urlpatterns = [
    path('gbvh4457d', views.comingsoon, name="comingsoon"),
    path('', views.home, name="home"),
    path('otpjdafahlsd/', views.otp, name="send_otp"),
    path('confirmfsdakjfk/', views.confirm, name="confirm"),
    path('submitsadlkf/', views.send_otp, name='otp'),
    path('verifyfsdajdf/', views.verify, name='verify'),
    path('verify/submitfasdf/', views.verify_otp, name='verify_otp'),
    path('registerfasdf/', views.register, name='register'),
    path('register/submitsdfas/', views.SaveData, name='SaveData'),
    path('managebookingdsafdsfadsf42/', views.manangebooking, name='managebooking'),
    path('manage_booking541f4rfqegwh5j/', views.manage_booking_page, name='manage_booking'),
    path('verify_otp514fvgwhgq3h/', views.verifiy_otp_manage_booking, name='verifiy_otp_manage_booking'),
    path('backup/users34g4qq43',views.backupData_users),
    path('backup/verifiedusersffagafg4q4',views.backupData_verified_users),
    path('backup/transactionsgadg45',views.backupData_transactions),
    path('dletesfdsdfar32gafa43',views.delete_kardega),
    path('w2kmfu7rhsdafaer4',views.all_verified_users),
] 
