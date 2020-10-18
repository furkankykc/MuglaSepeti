from django.urls import path
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from muglaSepetiApp import views
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from muglaSepetiApp.forms import LoginForm

urlpatterns = [
    path('', views.index, name='home'),
    path('checkout', views.checkout, name='checkout'),
    path('restaurants', views.companies, name='companies'),
    path('apply_cancel', views.apply_cancel, name='apply_cancel_note'),
    path('print/<int:pk>', views.print_payment, name='print'),
    path('do_comment', views.do_comment, name='do_comment'),
    path('shop', views.index, name='shop'),
    path('restaurants/<slug:company_slug>/details/<int:entry_id>', views.entry_details, name='food'),
    path('login/', views.RememberLoginView.as_view(
        authentication_form=LoginForm, redirect_authenticated_user=True
    ), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('cart/delete/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_delete, name='cart_delete'),
    path('cart/count/add/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_count_add, name='cart_add'),
    path('cart/count/minus/bucket/<int:bucket_pk>/list/<int:list_pk>', views.cart_count_minus, name='cart_minus'),
    path('cart/collation/<slug:bucket_entry_pk>', views.cart_apply_collation, name='collation'),

    path('profile/update/info', views.update_info, name='update_info'),
    path('profile/update/user', views.update_user, name='update_user'),
    path('profile/change/pass', views.change_pass, name='change_pass'),
    path('profile/add/address', views.add_address, name='add_address'),

    path('about', views.about, name='about'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('logout', views.logout, name='logout'),

    path('check/<int:pk>', views.check, name='check'),
    path('order/<int:pk>', views.order, name='order'),
    path('order/', views.order_food, name='order_food'),
    path('ontheway/<int:pk>', views.ontheway, name='on_the_way'),
    path('deliver/<int:pk>', views.deliver, name='deliver'),
    path('cancel/<int:pk>', csrf_exempt(views.cancel), name='cancel'),
    path('get_data/', views.get_more_tables, name='get_more_data'),
    path('restaurants/<slug:company_slug>', views.company_menu, name='company_menu'),
    path('restaurants/<slug:company_slug>/category/<int:category_id>', views.company_menu, name='company_category'),
    path(r'service-worker.js', cache_control(max_age=2592000)(TemplateView.as_view(
        template_name="service-worker.js",
        content_type='application/javascript',
    )), name='service-worker.js'),
]
