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

    path("edit_camera",views.editCAM,name="edit_camera"),
    path("edit_alarmdetails",views.editALARMDETAILS,name="edit_alarmdetails"),
    path("add_roi",views.camera_adding_roi,name="add_roi"),
    path("edit_roi",views.camera_edit_roi,name="edit_roi"),
    path("delete_roi",views.camera_delete_roi,name="delete_roi"),
    path("add_cr_data",views.camera_add_cr_data,name="add_cr_data"),
    path("edit_crdata",views.camera_editCRroi,name="edit_crdata"),
    path("delete_cr_data",views.camera_delete_cr_data,name="delete_cr_data"),
    path("delete_crfullframe_data",views.delete_crfullframe_data,name="delete_crfullframe_data"),
    path("add_tc_data",views.camera_add_tc_data,name="add_tc_data"),
    path("edit_tcdata",views.camera_edittcroi,name="edit_tcdata"),
    path("delete_tc_data",views.camera_delete_tc_data,name="delete_tc_data"),
    path("get_ra_camera_details",views.ra_camera_details,name="get_ra_camera_details"),
    path("get_ra_camera_details/<id>",views.ra_camera_details,name="get_ra_camera_details/<id>"),
    path("delete_ra_camera/<id>",views.delete_ra_cameras,name="delete_ra_camera/<id>"),
    path("delete_multiple_camera",views.delete_multiple_camera,name="delete_multiple_camera"),
    path("analytics_status/<id>/<status>",views.analyt,name="analytics_status/<id>/<status>"),
    path("coin_id_start_record",views.coin_id_start_record,name="coin_id_start_record"),
    path("get_coin_violationData",views.CoinIDViolationData,name="get_coin_violationData"),
    path("getviolationvideo/<video_name>",views.CoinviolationVideo,name="getviolationvideo/<video_name>"),
    path("getcoinidlist",views.COinidlist,name="getcoinidlist"),
    path("getcoinidcameralist",views.getcoinidcameralist,name="getcoinidcameralist"),
    path("add_firesmoke",views.add_firesmoke,name="add_firesmoke"),


    path("addfsddata",views.Newformatefsddataadding,name="addfsddata"),
    path("edit_fsd",views.edit_fsd,name="edit_fsd"),
    path("addfsdstaticparameters",views.addfsdstaticparameters,name="addfsdstaticparameters"),
    path("delete_fsddata",views.delete_fsddata,name="delete_fsddata"),
    path("edit_preset",views.edit_preset,name="edit_preset"),
    path("delete_preset",views.delete_preset,name="delete_preset"),
    path("delete_firesmoke",views.delete_firesmoke,name="delete_firesmoke"),

]