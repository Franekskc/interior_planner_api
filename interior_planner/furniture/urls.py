from django.urls import path
from . import views

urlpatterns = [
    path('furniture/', views.furniture_list, name='furniture-list'),
]