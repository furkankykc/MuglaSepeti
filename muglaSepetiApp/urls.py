from django.contrib import admin
from django.urls import path

from muglaSepetiApp import views
from django.contrib.auth import views as auth_views

from muglaSepetiApp.forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('checkout', views.checkout, name='checkout'),
    path('restaurants', views.companies, name='companies'),
    path('login/', views.RememberLoginView.as_view(
        authentication_form=LoginForm
    ), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='assets/forgot-password.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('check/<int:pk>', views.check, name='check'),
    path('ontheway/<int:pk>', views.ontheway, name='on_the_way'),
    path('deliver/<int:pk>', views.deliver, name='deliver'),
    path('cancel/<int:pk>', views.cancel, name='cancel'),
    path('get_data/', views.get_more_tables, name='get_more_data'),
    path('restaurants/<slug:cmp_slug>', views.company_menu, name='company_menu'),
]
