from django.urls import path
from . import views

urlpatterns = [
    # Login and Registration
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Devices
    # path('devices/manage/list?<int:page>&<str:sort_by>&<int:elems>', views.devices_list, name='devices_list'),
    path('devices/manage/list', views.devices_list, name='devices_list'),
    path('devices/manage/requests', views.devices_requests, name='devices_requests'),
    path('devices/manage/api_inspection', views.devices_api_inspection, name='devices_api_inspection'),
    path('devices/manage/add', views.devices_add_form, name='devices_add_form'),

    path('devices/settings/general_settings', views.devices_general_settings, name='devices_general_settings'),
    path('devices/settings/api_settings', views.devices_api_settings, name='devices_api_settings'),

    # Cameras
    path('cameras/manage/list', views.cameras_list, name='cameras_list'),
    path('cameras/manage/detection_areas', views.cameras_detection_areas, name='cameras_detection_areas'),
    path('cameras/manage/livestream', views.cameras_livestream, name='cameras_livestream'),
    path('cameras/manage/add', views.cameras_add_form, name='cameras_add_form'),

    path('cameras/manage/general_settings', views.cameras_general_settings, name='cameras_general_settings'),
    path('cameras/manage/streaming_settings', views.cameras_streaming_settings, name='cameras_streaming_settings'),

    # Users
    path('users/manage/list', views.users_list, name='users_list'),
    path('users/manage/roles', views.users_role_list, name='users_role_list'),
    path('users/manage/bans', views.users_ban_list, name='users_ban_list'),


    # Misc.
    path('misc/quick_start', views.misc_quick_start, name='misc_quick_start'),
    path('misc/help', views.misc_help, name='misc_help'),
]
