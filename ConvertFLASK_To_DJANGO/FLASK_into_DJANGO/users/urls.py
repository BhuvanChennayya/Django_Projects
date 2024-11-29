from django.urls import path
from . import views

urlpatterns=[
    path("signup",views.signup,name="signup"),
    path("profile",views.admin_profile,name="profile"),
    path("logout",views.logout,name="logout"),
    path("changepassword",views.change,name="changepassword"),
    path("forgot_password",views.forgot_password,name="forgot_password"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("update_user_profile",views.update_user,name="update_user_profile"),
    path("profile_picture/<filename>",views.profile_pic,name="profile_picture/<filename>"),
    path("update_profile_picture",views.update_profile_picture,name="update_profile_picture"),

]