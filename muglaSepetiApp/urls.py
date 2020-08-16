from django.contrib import admin
from django.urls import path

from muglaSepetiApp import views

urlpatterns = [
    path('', views.test),
    path('check/<int:pk>', views.check, name='check'),
    path('ontheway/<int:pk>', views.ontheway, name='on_the_way'),
    path('deliver/<int:pk>', views.deliver, name='deliver'),
    path('cancel/<int:pk>', views.cancel, name='cancel'),
    path('get_data/', views.get_more_tables, name='get_more_data'),
]
