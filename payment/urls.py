from django.urls import path, re_path
from . import views

urlpatterns = [
    path('error/', views.payment_error, name='payment_error'),
    path('response/', views.payment_response, name='payment_response'),
    path('status/', views.payment_response, name="payment_status"),
    path('success/', views.success, name="payment_success"),
    path('get_status/', views.get_status_ajax, name="get_status_ajax")

    # path('status/',views.payment_status,name='payment_status'),
    # re_path(r'^get_status_ajax/$', views.get_status_ajax, name='get_status_ajax'),
]
