from django.urls import path
from . import views

urlpatterns=[
    path("get_latest_five_hours_data",views.get_latest_five_hours_data,name="get_latest_five_hours_data"),
    path("get_latest_five_hours_PA_NPA_data",views.get_latest_five_hours_PA_NPA_data,name="get_latest_five_hours_PA_NPA_data"),
    path("slots_status_details/VPMS/<val>",views.slots_status_details,name="slots_status_details/VPMS/<val>"),
    path("cameralist",views.get_cameralist,name="cameralist"),
    path("all_camera_slot_details",views.all_camera_slot_details,name="all_camera_slot_details"),
    path("slot_details",views.slot_details,name="slot_details"),
    path("slot_details/<val>",views.slot_details,name="slot_details/<val>"),
    path("PA_history",views.get_PA_history,name="PA_history"),
    path("PA_history/<flag>",views.get_PA_history,name="PA_history/<flag>"),
    path("violations_data",views.get_VPMS_history,name="violations_data"),
    path("list_PA_slots",views.PA_Slots,name="list_PA_slots"),
    path("latest_parking_history",views.latest_history,name="latest_parking_history"),
    path("datewise_camera_list",views.datewise_camera_list,name="datewise_camera_list"),
    path("datewise_history",views.datewise_violation,name="datewise_history"),
#                       """For Violations excel sheets """
    path("create_violation_excelVPMS",views.create_violation_excelVPMS,name="create_violation_excelVPMS"),
    path("VPMS_violation_excel_download",views.VPMS_violation_excel_download,name="VPMS_violation_excel_download"),
    path("VPMSimage/VPMS/PA/<image_file>'",views.get_img_bbox,name="VPMSimage/VPMS/PA/<image_file>'"),
    path("VPMSimage/VPMS/PA/<image_file><roiname>/",views.get_img_bbox,name="VPMSimage/VPMS/PA/<image_file>/<roiname>"),
    path("VPMSimage/VPMS/NPA/<image_file>'",views.NPAimage,name="VPMSimage/VPMS/NPA/<image_file>'"),
    path("VPMSimage/VPMS/NPA/<image_file><roiname>/",views.NPAimage,name="VPMSimage/VPMS/NPA/<image_file>/<roiname>"),

]