from django.urls import path
from . import views

urlpatterns = [
    # Device endpoints
    path('device/list', views.device_list, name='device_list'),
    path('device/detail/<int:id>/', views.device_detail, name='device_detail'),
    path('device/create/<str:token>/', views.device_create, name='device_create'),
    path('device/update/<int:id>/', views.device_update, name='device_update'),
    path('device/delete/<int:id>/', views.device_delete, name='device_delete'),

    # Camera endpoints
    path('camera/list', views.camera_list, name='camera_list'),
    path('camera/detail/<int:id>/', views.camera_detail, name='camera_detail'),
    path('camera/create', views.camera_create, name='camera_create'),
    path('camera/update/<int:id>/', views.camera_update, name='camera_update'),
    path('camera/delete/<int:id>/', views.camera_delete, name='camera_delete')
]
