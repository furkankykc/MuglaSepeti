from django.contrib import admin
from django.urls import path

from muglaSepetiApp import views

urlpatterns = [
    path('', views.test),
]
