from django.urls import path
from . import views

urlpatterns=[
    path("start_firesmoke",views.start_firesmoke,name="start_firesmoke"),
    path("stop_firesmokeapp",views.stop_application_1_phaseoneapp,name="stop_firesmokeapp"),
    path("getFireVideo/<vidoename>",views.firevidoe,name="getFireVideo/<vidoename>"),
    path("GETFIRESMOKEIMAGE/<imagename>",views.FIREANDSMOKEDUSTIMAGE,name="GETFIRESMOKEIMAGE/<imagename>"),
    path("DeleteFireViolation/<id>",views.DeleteFIREviolation,name="DeleteFireViolation/<id>"),
    path("FIRESMOKEverification/<id>/<flag>",views.FIRESMOKEVERIFICATIONviolation,name="FIRESMOKEverification/<id>/<flag>"),
    path("FSDLiveviolationdata",views.FSDLiveviolationdata,name="FSDLiveviolationdata"),
    path("FSDLiveviolationdata/<camera_name>",views.FSDLiveviolationdata,name="FSDLiveviolationdata/<camera_name>"),
    path("datewiseFiresmoke/<cameraname>",views.datewiseFiresmoke,name="datewiseFiresmoke/<cameraname>"),
    path("datewiseFiresmoke/<pagenumber>/<page_limit>",views.datewiseFiresmoke,name="datewiseFiresmoke//<pagenumber>/<page_limit>"),
    path("datewiseFiresmoke/<cameraname>/<pagenumber>/<page_limit>",views.datewiseFiresmoke,name="datewiseFiresmoke/<cameraname>/<pagenumber>/<page_limit>"),
    path("Firecameradetails",views.Firecameradetails,name="Firecameradetails"),
    path("Firedepartmentdetails",views.Firedepartmentdetails,name="Firedepartmentdetails"),
    path("create_violation_excelFSD",views.create_violation_excelFSD,name="create_violation_excelFSD"),
    path("create_violation_excelFireSmoke",views.create_violation_excelFireSmoke,name="create_violation_excelFireSmoke"),
    path("firesmokeviolation_excel_download",views.firesmokeviolation_excel_download,name="firesmokeviolation_excel_download"),

]