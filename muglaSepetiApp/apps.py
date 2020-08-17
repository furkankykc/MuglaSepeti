from django.apps import AppConfig

from django.contrib.admin.apps import AdminConfig


class MuglasepetiappConfig(AppConfig):
    name = 'muglaSepetiApp'


class MyAdminConfig(AdminConfig):
    default_site = 'muglaSepetiApp.admin.CustomAdminSite'
