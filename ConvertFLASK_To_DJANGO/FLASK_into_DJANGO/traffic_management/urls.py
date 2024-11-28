from django.urls import path
from . import views

urlpatterns=[
    path("capture_image",views.capture_image ,name="capture_image"),
    path("latest_hour_TJM_data",views.latest_hour_TJM_data ,name="latest_hour_TJM_data"),
    path("test_todays_data",views.test_todays_data ,name="test_todays_data"),
    path("overall_todays_TJM_data",views.overall_to222days_TJM_data ,name="overall_todays_TJM_data"),
    path("live_traffic_jam_data",views.live_traffic_jam_data ,name="live_traffic_jam_data"),
    path("live_trafficjam_data",views.live_trafficjam_data ,name="live_trafficjam_data"),
    path("TJM/rois_list",views.get_rois_list ,name="TJM/rois_list"),
    path("TJM/datewise_rois_list",views.datewise_rois_list ,name="TJM/datewise_rois_list"),
    path("TJM/cameralist",views.get_cameralist ,name="TJM/cameralist"),
    path("TJM/datewise_camera_list",views.datewise_camera_list ,name="TJM/datewise_camera_list"),
    path("latest_five_hours_traffic_jam",views.updated_latest_five_hours_traffic_jam ,name="latest_five_hours_traffic_jam"),
    path("latest_traffic_jam_history",views.latest_history ,name="latest_traffic_jam_history"),
    path("tjm_datewise_history",views.tj_datewise_history ,name="tjm_datewise_history"),
    path("datewise_hours_traffic_jam",views.datewise_hours_traffic_jam ,name="datewise_hours_traffic_jam"),
    path("trafficjamlivedata",views.trafficjamlivedata ,name="trafficjamlivedata"),
    path("trafficjamlivedata/cameraname/<camera_name>",views.trafficjamlivedata ,name="trafficjamlivedata/cameraname/<camera_name>"),
    path("trafficjamlivedata/department/<department_name>",views.trafficjamlivedata ,name="trafficjamlivedata/department/<department_name>"),
    path("trafficjamDatewise",views.DATEWISERA ,name="trafficjamDatewise'"),
    path("trafficjamDatewise/<cameraname>",views.DATEWISERA ,name="trafficjamDatewise/<cameraname>'"),
    path("trafficjamDatewise/<pagenumber>/<page_limit>",views.DATEWISERA ,name="trafficjamDatewise/<pagenumber>/<page_limit>'"),
    path("trafficjamDatewise/<cameraname>/<pagenumber>/<page_limit>",views.DATEWISERA ,name="trafficjamDatewise/<cameraname>/<pagenumber>/<page_limit>'"),
    path("TJMimage/<image_file>",views.TJMIMage ,name="TJMimage/<image_file>"),
    path("TJMimage/<roiname>/<image_file>",views.TJMIMage ,name="TJMimage/<roiname>/<image_file>"),

]