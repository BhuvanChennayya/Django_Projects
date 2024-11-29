from django.urls import path
from . import views

urlpatterns=[
    path("connect_and_configure",views.connect_and_configure,name="connect_and_configure",)
 
]