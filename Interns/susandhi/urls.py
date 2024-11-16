from django.urls import path
from . import views

urlpatterns=[
    path("Main/",views.Main,name="Main Page"),
    path('insert_intern/',views.insert_intern, name='insert_intern'),
    path('create_intern/',views.create_intern, name='create_intern'),
    path('get_all_person/delete_intern/<int:id>/', views.delete_intern, name='intern_details'),
    path('delete/<int:id>/', views.delete, name='delete intern'),
    path('get_all_person/update_intern/<int:id>/', views.update_intern, name='update_intern'),
    path('update/<int:id>/', views.update, name='update intern'),
    path('get_all_person/',views.get_all_person,name='get_all_person'),
    path('get_all_person/intern_details/<int:id>/', views.intern_details, name='intern_details'),
    
]