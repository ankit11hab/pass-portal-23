from django.urls import path, re_path
from . import views

urlpatterns = [
    path('errordsjkdfasdf88/', views.payment_error, name='payment_error'),
#     path('mail/', views.generate_qr_code, name='mail'),
    path('responsefsadfnjlasufo8/', views.payment_response, name='payment_response'),
    path('statusfaskdfla88jfii7/', views.payment_response, name="payment_status"),
    path('get_verified_detailsjkfhkef743jh2/',
         views.get_verified_details, name="get_verified_details"),
    path('get_payment_detailsafjjdf78/', views.get_payment_details,
         name="get_payment_details"),
    path('successfsdhfjgasdf682rqa/', views.success, name="payment_success"),
    path('get_statusfsadhjfyu8/', views.get_status_ajax, name="get_status_ajax"),
    path('under_processdajsfhqwte6/', views.under_process, name='UnderProcess'),
    # path('qrdsfasdfaswr3235r/<str:email>/<str:id>', views.generate_qr_code),
    # path('test',views.mail_all),
    # path('addmember',views.copy_collection),
    # path('all_ar',views.allqr)


    # path('status/',views.payment_status,name='payment_status'),
    # re_path(r'^get_status_ajax/$', views.get_status_ajax, name='get_status_ajax'),
]
