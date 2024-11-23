from django.urls import path
from . import views

urlpatterns=[
    path("PPEviolationCount",views.PPEviolationCount,name="PPEviolationCount"),
    path("CrashHelmentviolationCount",views.CrashHelmentviolationCount,name="CrashHelmentviolationCount"),
    path("RAviolationCount",views.RAviolationCount,name="RAviolationCount"),
    path("ProtectionZoneviolationCount",views.ProtectionZoneviolationCount,name="ProtectionZoneviolationCount"),
    path("CrowdCountviolationCount",views.CrowdCountviolationCount,name="CrowdCountviolationCount"),
    path("totalViolationCount",views.totalViolationCount,name="totalViolationCount"),
    path("get_cam_status_enable_cam_count",views.get_cam_status_enable_cam_count,name="get_cam_status_enable_cam_count"),
    path("get_solution_data_details",views.get_solution_data_details,name="get_solution_data_details"),
    path("get_current_date_violation_counts",views.get_current_date_violations,name="get_current_date_violation_counts"),
    path("disable_camera_details",views.disable_camera_details,name="disable_camera_details"),
    path("get_not_working_camera_details",views.get_not_working_camera_details,name="get_not_working_camera_details"),
    path("get_all_solns_enable_cam_details",views.get_all_solns_enable_cam_count,name="get_all_solns_enable_cam_details"),
    path("get_enble_ppe_violation_count",views.get_enble_ppe_violation_count,name="get_enble_ppe_violation_count"),
    path("to_get_today_data",views.to_get_today_data,name="to_get_today_data"),
    path("data_betweem_violations_count",views.data_betweem_violations_count,name="data_betweem_violations_count"),
    path("date_wise_violations_count",views.date_wise_given_violation_count,name="date_wise_violations_count"),
    path("data_between_date",views.data_between_date,name="data_between_date"),
    path("cam_wise_PPE_violations_count",views.ppe_violations_count_cam_wise,name="cam_wise_PPE_violations_count"),
    path("cam_wise_TC_violations_details",views.TC_violations_count_cam_wise,name="cam_wise_TC_violations_details"),
    path("cam_wise_RA_violations_count",views.RA_violations_count_cam_wise,name="cam_wise_RA_violations_count"),
    path("cam_wise_truck_reversal_RA_violations_count",views.cam_wise_truck_reversal_RA_violations_count,name="cam_wise_truck_reversal_RA_violations_count"),
    path("cam_wise_CR_violations_count",views.CR_violations_count_cam_wise,name="cam_wise_CR_violations_count"),
    path("cam_wise_PPE_Crash_helmet_violations_count",views.ppe_Crash_helmet_violations_count_cam_wise,name="cam_wise_PPE_Crash_helmet_violations_count"),
    path("FIREviolationCount",views.FIREviolationCount,name="FIREviolationCount"),


]