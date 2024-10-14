from django.urls import path
from . import views

urlpatterns = [
    path('',  views.getRoutes),
    path('channels/', views.getChannels),
    path('channels/<str:pk>/', views.getChannel),
]