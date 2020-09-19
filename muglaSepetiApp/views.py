from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from muglaSepetiApp.forms import RegisterForm, ChangeUserForm, ChangeProfileForm, CreateAddressForm, ChangePasswordForm
from muglaSepetiApp.models import Bucket, Company, Menu, Entry, FoodCategory, Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm


def test(request):
    page_url = "assets/index.html"
    return render(request, template_name=page_url)


def index(request):
    context = {

    }
    return render(request, template_name='muglaSepeti/index.html', context=context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, template_name='registration/register.html', context=context)


def profile(request):
    profileForm = ChangeProfileForm(instance=request.user.profile)
    userForm = ChangeUserForm(instance=request.user)
    addressForm = CreateAddressForm()
    passwordForm = ChangePasswordForm(request.user)
    context = {
        'user_form': userForm,
        'profile_form': profileForm,
        'address_form': addressForm,
        'password_form': passwordForm,
    }
    return render(request, template_name='registration/profile.html', context=context)


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(reverse('home'))


@login_required(login_url='login')
def checkout(request):
    context = {
    }
    return render(request, template_name='muglaSepeti/checkout.html', context=context)


def cart_delete(request, bucket_pk, list_pk):
    bucket = Bucket.objects.get(profile__user=request.user, pk=bucket_pk)
    bucket_item = bucket.order_list.get(pk=list_pk)
    if bucket_item:
        bucket.order_list.remove(bucket_item)
        bucket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_count_add(request, bucket_pk, list_pk):
    bucket = Bucket.objects.get(profile__user=request.user, pk=bucket_pk)
    bucket_item = bucket.order_list.get(pk=list_pk)
    if bucket_item:
        if bucket_item.count < 99:
            bucket_item.count = bucket_item.count + 1
            bucket_item.save()
            bucket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_count_minus(request, bucket_pk, list_pk):
    bucket = Bucket.objects.get(profile__user=request.user, pk=bucket_pk)
    bucket_item = bucket.order_list.get(pk=list_pk)
    if bucket_item:
        if bucket_item.count > 1:
            bucket_item = bucket.order_list.get(pk=list_pk)
            bucket_item.count = bucket_item.count - 1
            bucket_item.save()
            bucket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def entry_details(request, company_slug, entry_id):
    # company = Company.objects.get(slug=company_slug)
    entry = Entry.objects.get(company__slug=company_slug, pk=entry_id)
    return render(request, template_name='muglaSepeti/food_details.html', context={'entry': entry})


def companies(request):
    context = {
        'companies': Company.get_open_companies()
    }
    return render(request, template_name='muglaSepeti/company_list.html', context=context)


@login_required(login_url='login')
def order_food(request):
    order_now = False
    if request.method == 'POST':
        if 'order_now' in request.POST:
            order_now = True
        quantity = request.POST['quantity']
        entry_id = request.POST['entry_id']
        bucket = request.user.profile.get_bucket()
        entry = Entry.objects.get(id=entry_id)

        bucket.add_entry(entry, int(quantity))
        # [print(i.count) for i in bucket.order_list.all()]
    if order_now:
        return HttpResponseRedirect(reverse('checkout'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order(request, pk):
    bucket = Bucket.objects.get(pk=pk)
    bucket.order(request.user.profile)
    if request.POST:
        payment_type = request.POST['payment_type']
        order_note = request.POST['order_note']
        bucket.payment_type = payment_type
        bucket.delivery_note = order_note
        print(payment_type)
    bucket.save()

    print("Sipariş edildi")
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def check(request, pk):
    Bucket.objects.get(pk=pk).check_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ontheway(request, pk):
    Bucket.objects.get(pk=pk).order_on_the_way()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deliver(request, pk):
    Bucket.objects.get(pk=pk).deliver_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cancel(request, pk):
    Bucket.objects.get(pk=pk).cancel_order()
    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_user(request):
    if request.method == 'POST':
        obj = get_object_or_404(User, username=request.user.username)
        form = ChangeUserForm(request.POST, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            u = form.save(commit=False)
            u.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_info(request):
    if request.method == 'POST':
        obj = get_object_or_404(User, username=request.user.username)

        form = ChangeProfileForm(request.POST, instance=obj.profile)
        if form.is_valid():
            cd = form.cleaned_data
            u = form.save(commit=False)
            u.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_address(request):
    if request.method == 'POST':
        form = CreateAddressForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            print("cdddd = ", cd)
            address = form.save(commit=False)
            address.owner = request.user.profile
            address.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# not used only for example
def get_more_tables(request):
    increment = int(request.GET['append_increment'])
    increment_to = increment + 10
    qs = Bucket.objects.all()
    if request.user.is_superuser:
        return render(request, 'get_more_data.html', {'order': qs})
    return render(request, 'get_more_data.html', {'order': qs.filter(company__owner=request.user, is_ordered=True)})


def one_page_companies(request, company_id=0):
    open_companies = Company.get_open_companies()
    active_menu_ids = open_companies.values('active_menu')
    active_menus = Menu.objects.filter(id__in=active_menu_ids)
    active_menus = active_menus.all() if company_id == 0 else active_menus.filter(company_id=company_id)
    active_menus_entry_ids = active_menus.values_list('entry_list', flat=True)
    entries = Entry.objects.filter(id__in=active_menus_entry_ids)
    context = {
        'companies': open_companies,
        'menu': active_menus,
    }


def company_menu(request, company_slug, category_id=None):
    company = Company.objects.get(slug=company_slug)
    category_ids = company.active_menu.entry_list.values_list('category', flat=True).distinct()
    categories = FoodCategory.objects.filter(id__in=category_ids)
    if (category_id):
        entries = company.active_menu.entry_list.filter(category=category_id)
    else:
        entries = company.active_menu.entry_list.all()
    context = {
        'company': company,
        'categories': categories,
        'entries': entries,
        'category_id': category_id,
    }
    return render(request, template_name='muglaSepeti/company_page.html', context=context)


class RememberLoginView(LoginView):
    # def get(self, request, *args, **kwargs):
    #
    #     request.session.set_test_cookie()
    #     super(RememberLoginView, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            request.session.set_test_cookie()
            return self.form_valid(form)
        else:

            request.session.set_test_cookie()
            return self.form_invalid(form)
