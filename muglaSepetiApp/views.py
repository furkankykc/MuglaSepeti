from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from muglaSepetiApp.forms import RegisterForm, ChangeUserForm, ChangeProfileForm, CreateAddressForm, ChangePasswordForm, \
    RatingForm
from muglaSepetiApp.models import Bucket, Company, Menu, Entry, FoodCategory, Profile, SiteConfig, Annoucment, \
    BucketEntry, BucketCollation, CollationNode
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import PasswordChangeForm

from django.utils.translation import ugettext as _


def test(request):
    page_url = "assets/index.html"
    return render(request, template_name=page_url)


def index(request):
    context = {
        'companies': Company.objects.only('name', 'logo', 'description', 'slug').exclude(logo__exact='',
                                                                                         logo__isnull=False)
    }
    return render(request, template_name='muglaSepeti/index.html', context=context)


def about(request):
    context = {

    }
    return render(request, template_name='muglaSepeti/about.html', context=context)


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
    messages.success(request, _("Başarıyla Kayıt oldunuz. Devam etmek için giriş yapınız"))
    return render(request, template_name='registration/register.html', context=context)


@login_required(login_url='login')
def profile(request):
    profileForm = ChangeProfileForm(instance=request.user.profile)
    userForm = ChangeUserForm(instance=request.user)
    addressForm = CreateAddressForm()
    passwordForm = ChangePasswordForm(request.user)
    ratingForm = RatingForm()
    context = {
        'user_form': userForm,
        'profile_form': profileForm,
        'address_form': addressForm,
        'password_form': passwordForm,
        'rating_form': ratingForm,
    }
    return render(request, template_name='registration/profile.html', context=context)


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, _("Başarıyla çıkış yapıldı"))
    return redirect(reverse('home'))


@login_required(login_url='login')
def checkout(request):
    context = {
    }
    return render(request, template_name='muglaSepeti/checkout.html', context=context)


@login_required(login_url='login')
def cart_delete(request, bucket_pk, list_pk):
    bucket = Bucket.objects.get(profile__user=request.user, pk=bucket_pk)
    bucket_item = bucket.order_list.get(pk=list_pk)
    if bucket_item:
        bucket.order_list.remove(bucket_item)
        bucket.save()
        messages.success(request, "Ürün başarıyla silindi")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def apply_cancel(request):
    if request.method == "POST":
        if 'cancel_note' in request.POST:
            cancel_note = request.POST['cancel_note']
            order_id = request.POST['id']
            print(f'cancel note is : {cancel_note}')


def cart_apply_collation(request, bucket_entry_pk):
    bucket_entry = BucketEntry.objects.get(pk=bucket_entry_pk)
    if request.method == "POST":
        print(f"{bucket_entry.pk} collation setted")
        for collation in bucket_entry.entry.collation.collation_list.all():
            if str(collation.pk) in request.POST:
                print(f"{collation.pk}:{request.POST[str(collation.pk)]}")
                bucket_entry.set_collation(collation.pk)


# todo minus add düzeltilip model ile ilgili olan işlemler modele alınacak, var olan add_entry fonksiyonu kullanılacak
@login_required(login_url='login')
def cart_count_add(request, bucket_pk, list_pk):
    bucket = Bucket.objects.get(profile__user=request.user, pk=bucket_pk)
    bucket_item = bucket.order_list.get(pk=list_pk)
    if bucket_item:
        if bucket_item.count < 99:
            bucket_item.count = bucket_item.count + 1
            bucket_item.save()
            bucket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# todo minus add düzeltilip model ile ilgili olan işlemler modele alınacak, var olan add_entry fonksiyonu kullanılacak
@login_required(login_url='login')
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
        'companies': Company.get_open_companies(),
        'annoucments': Annoucment.objects.filter(is_active=True)
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
        try:
            bucket.add_entry(entry, int(quantity))
            messages.success(request, "{}x{} {}".format(quantity, entry.name, _("sepete eklendi")))
        except ValueError as e:
            messages.error(request, _(
                "Birden fazla restorandan aynı anda sipariş veremezsiniz. Lütfen aynı restorandan sipariş verin yada "
                "sepetinizi temizleyin"))
        # [print(i.count) for i in bucket.order_list.all()]
    if order_now:
        return HttpResponseRedirect(reverse('checkout'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def order(request, pk):
    bucket = Bucket.objects.get(pk=pk)
    bucket.order(request.user.profile)
    if request.POST:
        payment_type = request.POST['payment_type']
        order_note = request.POST['order_note']
        bucket.payment_type = payment_type
        bucket.delivery_note = order_note
        bucket.save()
        messages.success(request, "{} {}".format(bucket.company.name,
                                                 _("firmasından almış olduğunuz yemekler başarıyla sipariş edildi.")))

        # print("Sipariş edildi")
        # redirect back to where it comes from

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def print_payment(request, pk):
    return render(request, "components/print.html", {"document": Bucket.objects.get(pk=pk)})


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
    bo = Bucket.objects.get(pk=pk)
    if request.method == "post":
        bo.cancel_note = request.POST["cancel_note"]

    bo.cancel_note = request.POST["cancel_note"]
    bo.cancel_order()
    print(request.POST["cancel_note"])

    # redirect back to where it comes from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def update_user(request):
    if request.method == 'POST':
        obj = get_object_or_404(User, username=request.user.username)
        form = ChangeUserForm(request.POST, instance=obj)
        if form.is_valid():
            cd = form.cleaned_data
            u = form.save(commit=False)
            u.save()
            messages.success(request, "Profiliniz başarıyla güncellendi")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#")


@login_required(login_url='login')
def update_info(request):
    if request.method == 'POST':
        obj = get_object_or_404(User, username=request.user.username)

        form = ChangeProfileForm(request.POST, instance=obj.profile)
        if form.is_valid():
            cd = form.cleaned_data
            u = form.save(commit=False)
            u.save()

            messages.success(request, _("Profiliniz başarıyla güncellendi"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#")


@login_required(login_url='login')
def add_address(request):
    if request.method == 'POST':
        form = CreateAddressForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            address = form.save(commit=False)
            address.owner = request.user.profile
            address.save()

    messages.success(request, _("Adres başarıyla eklendi"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#")


@login_required(login_url='login')
def change_pass(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()

            messages.success(request, _("Şifreniz güncellendi"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#")


@login_required(login_url='login')
def do_comment(request):
    if request.method == 'POST':
        form = RatingForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            u = form.save(commit=False)
            u.bucket = Bucket.objects.get(pk=request.POST['bucket_id'])
            u.owner = request.user
            u.save()
            messages.success(request, _("Yorum başarıyla eklendi"))
        else:
            messages.success(request, _("Yorum yapılamadı"))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
    category_ids = []
    entries = None
    if company.active_menu is not None:
        category_ids = company.active_menu.entry_list.values_list('category', flat=True).distinct()

        if category_id:
            entries = company.active_menu.entry_list.filter(category=category_id)
        else:
            entries = company.active_menu.entry_list.filter(is_disabled=False)
    categories = FoodCategory.objects.filter(id__in=category_ids)
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

            messages.success(request, _("Başarıyla Giriş Yapıldı."))
            request.session.set_test_cookie()
            return self.form_valid(form)
        else:

            request.session.set_test_cookie()
            return self.form_invalid(form)
