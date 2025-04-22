from django.urls import path
from . import views

urlpatterns = [
    path('furniture/', views.furniture_list, name='furniture-list'),
    path('walls', views.WallTextureListView.as_view(), name='wall-texture-list'),
    path('floors', views.FloorTextureListView.as_view(), name='floor-texture-list'),
]