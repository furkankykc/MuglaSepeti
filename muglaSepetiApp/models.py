import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Sum
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.text import slugify

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
email_regex = RegexValidator(regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                             message="Email address must be entered in the format: 'example@mail.com'.")


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Address(models.Model):
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=500)
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ManyToManyField(Address, related_name='profile_address')
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True)
    email = models.CharField(validators=[email_regex], max_length=50, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    slug = models.SlugField(blank=True)
    active_menu = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='comp_active_menu')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True)
    email = models.CharField(validators=[email_regex], max_length=50, blank=True)
    address = models.CharField(max_length=500)
    open_at = models.TimeField(default=timezone.now)
    close_at = models.TimeField(default=timezone.now)
    is_open = models.BooleanField(default=False)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    tripadvisor = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    pinterest = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def get_is_open(self):

        curr_hour = timezone.now().hour
        curr_minute = timezone.now().minute
        open_hour = self.open_at.hour
        open_minute = self.open_at.minute
        close_hour = self.close_at.hour
        close_minute = self.close_at.minute
        if self.is_open:
            if (curr_hour >= open_hour and curr_minute >= open_minute) and (
                    curr_hour <= close_hour and curr_minute <= close_minute):
                return True
        return False

    def __str__(self):
        return self.name


class FoodGroup(models.Model):
    class Meta:
        verbose_name = 'Menü Grubu'
        verbose_name_plural = 'Menü Grupları'

    name = models.CharField(max_length=20, verbose_name='isim')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='sahip')

    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    class Meta:
        verbose_name = 'Menü Kategorisi'
        verbose_name_plural = 'Menü Kategorileri'

    name = models.CharField(max_length=20, verbose_name='isim')
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name='kapak fotoğrafı')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='sahip')
    group = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='grup')

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image


class Entry(models.Model):
    class Meta:
        verbose_name = 'Menü Ürünü'
        verbose_name_plural = 'Menü Ürünleri'

    name = models.CharField(max_length=30, verbose_name='isim')
    detail = models.CharField(max_length=100, verbose_name='ürün detayı')
    price = models.FloatField(verbose_name='fiyat')
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name='kapak fotoğrafı')
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, verbose_name='Kategori')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_entry', verbose_name='sirket')

    @property
    def get_image(self):
        return self.image or self.category.image

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=50)
    entry_list = models.ManyToManyField(Entry)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class BucketEntry(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    count = models.IntegerField(default=1)

    def __str__(self):
        return '{}x{}'.format(self.count, self.entry.name)


class Bucket(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    delivery_note = models.CharField(max_length=500, blank=True)
    order_list = models.ManyToManyField(BucketEntry, blank=True)
    order_address = models.CharField(max_length=500)
    order_phone = models.CharField(max_length=500)
    checked_at = models.DateTimeField(blank=True, null=True)
    ordered_at = models.DateTimeField(blank=True, null=True)
    on_the_way_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_ordered = models.BooleanField(default=False, )
    is_checked = models.BooleanField(default=False)
    is_on_the_way = models.BooleanField(default=False, )
    is_delivered = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)

    PAYMENT_OPTIONS = (
        ('N', 'Nakit'),
        ('K', 'Kredi Kartı'),
    )
    payment_type = models.CharField(max_length=1, choices=PAYMENT_OPTIONS)

    def set_address(self, address: Address):
        self.order_address = address.location

    def set_phone(self):
        self.order_phone = self.profile.phone

    def order(self, address: Address):
        self.is_ordered = True
        self.ordered_at = timezone.now()
        self.set_phone()
        self.set_address(address)
        self.save()

    def check_order(self):
        if self.is_ordered:
            self.is_checked = True
            self.checked_at = timezone.now()
            self.save()

    def cancel_order(self):
        if self.is_ordered:
            self.is_checked = False
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.save()

    def order_on_the_way(self):
        if self.is_checked:
            self.is_on_the_way = True
            self.on_the_way_at = timezone.now()
            self.save()

    def deliver_order(self):
        if self.is_on_the_way:
            self.is_delivered = True
            self.delivered_at = timezone.now()
            self.save()

    def add_entry(self, entry: Entry, count: int = 1):
        obj, _ = self.order_list.get_or_create(entry_id=entry.id)
        obj.price = entry.price
        obj.entry = entry
        obj.count = obj.count + count
        obj.save()

    def get_borrow(self):
        sum = 0
        if self.order_list.exists():
            order_list = self.order_list.all()
            if order_list.count() > 0:
                sum = list(order_list.annotate(total_spent=Sum(
                    F('price') *
                    F('count'),
                    output_field=models.FloatField()
                )).aggregate(Sum('total_spent')).values())[0]
        return sum

    get_borrow.short_description = 'Fiyat'
    def __str__(self):
        return 'Accounting user {}'.format(self.profile.user.username)
