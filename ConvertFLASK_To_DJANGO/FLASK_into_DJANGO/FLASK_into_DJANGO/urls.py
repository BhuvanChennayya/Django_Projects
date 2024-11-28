"""FLASK_into_DJANGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import DashBoard.urls 
import camera_status_api.urls
import camera_coin_api.urls
import fire_smoke_config.urls
import parking_manage_data.urls
import POC.urls
import traffic_management.urls



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('DashBoard/', include(DashBoard.urls)),
    path('camera_status_api/', include(camera_status_api.urls)),
    path('camera_coin_api/', include(camera_coin_api.urls)),
    path('fire_smoke_config/', include(fire_smoke_config.urls)),
    path('parking_manage_data/', include(parking_manage_data.urls)),
    path('POC/', include(POC.urls)),
    path('traffic_management/', include(traffic_management.urls)),

]
