from django.urls import path
from . import views

urlpatterns = [
    path('furniture/', views.FurnitureListView.as_view(), name='furniture-list'),
    path('walls/', views.WallTextureListView.as_view(), name='wall-texture-list'),
    path('floors/', views.FloorTextureListView.as_view(), name='floor-texture-list'),

    path('furniture/<str:furniture_id>', views.FurnitureDetailView.as_view()),
    path('walls/<str:texture_id>', views.WallTextureDetailView.as_view()),
    path('floors/<str:texture_id>', views.FloorTextureDetailView.as_view()),
]