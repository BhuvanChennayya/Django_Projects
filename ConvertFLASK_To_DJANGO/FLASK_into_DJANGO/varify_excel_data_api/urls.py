from django.urls import path
from . import views

urlpatterns=[
    path("upload_cameras_excel",views.upload_cameras_excel,name="upload_cameras_excel"),
    path("get_camera_status_excel",views.get_camera_status_excel,name="get_camera_status_excel"),
    path("download_camera_status_sheet",views.excel_result,name="download_camera_status_sheet"),

]