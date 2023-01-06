from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'Login'),

    path('mail',views.generate_qr_code,name='QRcode'),
    path('postsignIn/', views.postsignIn),
    # path('signUp/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    # path('postsignIn/otp/',views.otp,name='otp'),
    path('postsignIn/submit/',views.otp,name='otp'),
    path('postsignIn/verify/',views.verify,name='verify'),
    path('postsignIn/verify/submit/',views.verify_otp,name='verify_otp'),
    path('postsignIn/register/',views.register,name='register'),
    path('postsignIn/register/submit/',views.SaveData,name='SaveData')
   

    # path('postsignUp/', views.postsignUp),

    

]