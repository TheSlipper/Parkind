from django.urls import path
from . import views

urlpatterns = [
    path('device/list', views.device_list, name='device_list'),
    path('device/detail/<int:id>/', views.device_detail, name='device_detail'),
    path('device/create', views.device_create, name='device_create'),
    path('device/update/<int:id>/', views.device_update, name='device_update'),
    path('device/delete/<int:id>/', views.device_delete, name='device_delete')
]
