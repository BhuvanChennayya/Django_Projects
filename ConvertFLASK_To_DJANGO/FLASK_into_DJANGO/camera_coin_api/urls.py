from django.urls import path
from . import views

urlpatterns=[
    path("CameraIMAGE",views.CameraIMAGE,name="CameraIMAGE"),
    path("CameraIMAGE/<id>",views.CameraIMAGE,name="CameraIMAGE"),
    path("check_license",views.checkingCamlicense,name="check_license"),
    path("get_camera_brand_details",views.get_camera_brand_details_all,name="get_camera_brand_details"),
    path("get_sample_rtsp",views.get_smaple_rtsp_all_brands,name="get_sample_rtsp"),
    path("license_count",views.license_count,name="license_count"),
    path("addcamerausingexcel",views.ADDCAMERASUSINGEXCEL,name="addcamerausingexcel"),
    path("add_camera",views.add_Acamera,name="add_camera"),
    path("add_camera_rtsp",views.add_Acamera_rtsp,name="add_camera_rtsp"),

]