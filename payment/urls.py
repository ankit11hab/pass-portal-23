from django.urls import path, re_path
from . import views

urlpatterns = [
    path('error/', views.payment_error, name='payment_error'),
#     path('mail/', views.generate_qr_code, name='mail'),
    path('response/', views.payment_response, name='payment_response'),
    path('status/', views.payment_response, name="payment_status"),
    path('get_verified_details/',
         views.get_verified_details, name="get_verified_details"),
    path('get_payment_details/', views.get_payment_details,
         name="get_payment_details"),
    path('success/', views.success, name="payment_success"),
    path('get_status/', views.get_status_ajax, name="get_status_ajax"),
    path('under_process/', views.under_process, name='UnderProcess'),
    # path('qrdsfasdfaswr3235r', views.generate_qr_code)
    # path('qrdsfasdfaswr3235r/<str:email>/<str:id>', views.generate_qr_code),
    # path('test',views.mail_all),
    # path('addmember',views.copy_collection),
    # path('all_ar',views.allqr)
    # path('all_emails',views.all_mails),
    path('send_emails',views.send_email)


    # path('status/',views.payment_status,name='payment_status'),
    # re_path(r'^get_status_ajax/$', views.get_status_ajax, name='get_status_ajax'),
]
