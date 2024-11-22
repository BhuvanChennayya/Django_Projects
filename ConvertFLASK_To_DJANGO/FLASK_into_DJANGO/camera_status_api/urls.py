from django.urls import path
from . import views

urlpatterns=[
    path("PPEviolationCount/",views.PPEviolationCount,name="PPEviolationCount/")
]