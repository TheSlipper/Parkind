from django.urls import path
from . import views


urlpatterns = [
    # Device endpoints
    path('device/list', views.device_list, name='device_list'),
    path('device/detail/<int:id>/', views.device_detail, name='device_detail'),
    path('device/create/<str:token>/', views.device_create, name='device_create'),
    path('device/update/<int:id>/', views.device_update, name='device_update'),
    path('device/delete/<int:id>/', views.device_delete, name='device_delete'),

    # Device request history
    path('device_request/list', views.device_request_list, name='device_request_list'),
    path('device_request/detail/<int:id>/', views.device_request_detail, name='device_request_detail'),
    path('device_request/delete/<int:id>/', views.device_request_delete, name='device_request_delete'),

    # ParkingArea
    path('detection_area/list', views.detection_area_list, name='detection_area_list'),
    path('detection_area/detail/<int:id>/', views.detection_area_detail, name='detection_area_detail'),
    path('detection_area/create', views.detection_area_create, name='detection_area_list'),
    path('detection_area/delete/<int:id>/', views.detection_area_delete, name='detection_area_delete'),

    # Camera endpoints
    path('camera/list', views.camera_list, name='camera_list'),
    path('camera/detail/<int:id>/', views.camera_detail, name='camera_detail'),
    path('camera/create', views.camera_create, name='camera_create'),
    path('camera/update/<int:id>/', views.camera_update, name='camera_update'),
    path('camera/delete/<int:id>/', views.camera_delete, name='camera_delete'),

    # Frame endpoints (used for streaming image)
    path('frame/<int:dev_id>/<int:cam_id>', views.frame_upload, name='frame_upload')
]
