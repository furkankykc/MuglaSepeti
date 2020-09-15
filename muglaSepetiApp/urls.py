from django.urls import path

from muglaSepetiApp import views
from django.contrib.auth import views as auth_views

from muglaSepetiApp.forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('checkout', views.checkout, name='checkout'),
    path('restaurants', views.companies, name='companies'),
    path('shop', views.index, name='shop'),
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

    path('cart/delete/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_delete, name='cart_delete'),
    path('cart/count/add/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_count_add, name='cart_add'),
    path('cart/count/minus/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_count_minus, name='cart_minus'),

    path('profile/update/info', views.update_info, name='update_info'),
    path('profile/update/user', views.update_user, name='update_user'),
    path('profile/change/pass', views.change_pass, name='change_pass'),
    path('profile/add/address', views.add_address, name='add_address'),

    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),
    path('check/<int:pk>', views.check, name='check'),
    path('order/<int:pk>', views.order, name='order'),
    path('ontheway/<int:pk>', views.ontheway, name='on_the_way'),
    path('deliver/<int:pk>', views.deliver, name='deliver'),
    path('cancel/<int:pk>', views.cancel, name='cancel'),
    path('get_data/', views.get_more_tables, name='get_more_data'),
    path('restaurants/<slug:cmp_slug>', views.company_menu, name='company_menu'),
]
