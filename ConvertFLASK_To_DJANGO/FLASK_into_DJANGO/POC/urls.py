from django.urls import path
from . import views

urlpatterns=[
    path("add_wheelcount_data",views.add_wheelcount_data,name="add_wheelcount_data"),
    path("edit_wheelcount_data",views.edit_wheelcount_data,name="edit_wheelcount_data"),
    path("delete_wheelcount_data",views.camera_delete_tc_data,name="delete_wheelcount_data"),
    path("start_wheelapplication",views.start_firesmoke,name="start_wheelapplication"),
    path("stop_wheelapplication",views.stop_application_1_phaseoneapp,name="stop_wheelapplication"),
    path("wheelcountlive",views.LIVEwheelcount,name="wheelcountlive"),
    path("wheelcountlive/<camera_name>",views.LIVEwheelcount,name="wheelcountlive/<camera_name>"),
    path("wheelcountlive/department/<department_name>",views.LIVEwheelcount,name="wheelcountlive/department/<department_name>"),
    path("wheelcountlive1",views.testwheelcount,name="wheelcountlive1"),
    path("wheelcountlive1/<camera_name>",views.testwheelcount,name="wheelcountlive1/<camera_name>"),
    path("wheelcountlive1/department/<department_name>",views.testwheelcount,name="wheelcountlive1/department/<department_name>"),
    path("wheelrotationlive",views.wheelroationlivedata,name="wheelrotationlive"),
    path("wheelrotationlive/<camera_name>",views.wheelroationlivedata,name="wheelrotationlive/<camera_name>"),
    path("wheelroationimage/<imagename>",views.wheelroationimage,name="wheelroationimage/<imagename>"),

]