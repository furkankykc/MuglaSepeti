import os

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Sum, Avg
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="{}: '+999999999'. {}.".format(_("Phone number must be entered in the format"),
                                                                    _("Up to 15 digits allowed")))
email_regex = RegexValidator(regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                             message="{}: 'example@mail.com'.".format(_("Email address must be entered in the format")))


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.id), filename)


class Address(models.Model):
    class Meta:
        verbose_name = _("Adress")
        verbose_name_plural = _("Addresses")

    name = models.CharField(max_length=30, verbose_name=_("name"))
    location = models.CharField(max_length=500, verbose_name=_("location"))
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='owner', verbose_name=_("owner"))

    def __str__(self):
        return self.name


class Profile(models.Model):
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("user"))
    address = models.ManyToManyField(Address, related_name='profile_address', verbose_name=_("adress"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("birth date"))
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True, verbose_name=_("phone number"))
    email = models.CharField(validators=[email_regex], max_length=50, blank=True, verbose_name=_("email address"))

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class GetCompanyOpen(models.Manager):
    def get_query_set(self):
        return super(GetCompanyOpen, self).get_query_set().filter(
            open_at__lte=timezone.now().time(), close_at__gt=timezone.now().time())


class Company(models.Model):
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("owner"))
    name = models.CharField(max_length=20, verbose_name=_("name"))
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_("logo"))
    slug = models.SlugField(blank=True, verbose_name=_("slug"))
    active_menu = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='comp_active_menu', verbose_name=_("active menu"))
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True, verbose_name=_("phone number"))
    email = models.CharField(validators=[email_regex], max_length=50, blank=True, verbose_name=_("email adress"))
    address = models.CharField(max_length=500, verbose_name=_("address"))
    open_at = models.TimeField(default=timezone.now, verbose_name=_("open time"))
    close_at = models.TimeField(default=timezone.now, verbose_name=_("close time"))
    is_open = models.BooleanField(default=False, verbose_name=_("is Open"), help_text=_(
        "if this box not checked your company wont open even if it currently open-hours"))
    instagram = models.URLField(blank=True, verbose_name=_("instagram address"))
    facebook = models.URLField(blank=True, verbose_name=_("facebook address"))
    twitter = models.URLField(blank=True, verbose_name=_("twitter address"))
    tripadvisor = models.URLField(blank=True, verbose_name=_("tripadvisor address"))
    youtube = models.URLField(blank=True, verbose_name=_("youtube address"))
    pinterest = models.URLField(blank=True, verbose_name=_("pinterest address"))

    # is_open_now = GetCompanyOpen()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    @classmethod
    def get_open_companies(cls):
        return cls.objects.filter(open_at__lte=timezone.now().time(), close_at__gt=timezone.now().time())

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

    def get_comments(self):
        return Bucket.objects.filter(company=self).order_by('-comment__time')

    def get_rating(self):
        rating = Bucket.objects.filter(company=self).aggregate(Avg('comment__rating'))['comment__rating__avg']
        return rating

    # get_is_open.short_description = _("Company Status")

    def __str__(self):
        return self.name


class FoodGroup(models.Model):
    class Meta:
        verbose_name = _('Product Group')
        verbose_name_plural = _('Product Groups')

    name = models.CharField(max_length=20, verbose_name=_("name"))
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("company"))

    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    name = models.CharField(max_length=20, verbose_name=_("name"))
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_("category image"))
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("owner"))
    group = models.ForeignKey(FoodGroup, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_("group"))

    def __str__(self):
        return self.name

    @property
    def get_image(self):
        return self.image


class Entry(models.Model):
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    name = models.CharField(max_length=50, verbose_name=_('name'))
    detail = models.CharField(max_length=100, verbose_name=_('detail'), blank=True, null=True)
    price = models.FloatField(verbose_name=_('price'))
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_('product image'))
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, verbose_name=_('category'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_entry', verbose_name=_('company'))

    @property
    def get_image(self):
        return self.image or self.category.image

    def get_food_rating(self):
        # todo get foot rating filter by entry id sum of total rating
        pass

    def __str__(self):
        return self.name


class Menu(models.Model):
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _("Menus")

    name = models.CharField(max_length=50, verbose_name=_("name"))
    entry_list = models.ManyToManyField(Entry, verbose_name=_("Entry list"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("company"))

    def __str__(self):
        return self.name


class BucketEntry(models.Model):
    class Meta:
        verbose_name = _("Bucket Product")
        verbose_name_plural = _("Bucket Products")

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, verbose_name=_("Product"))
    price = models.FloatField(default=0, verbose_name=_("Total Bucket Price"))
    count = models.IntegerField(default=1, verbose_name=_("Count"))

    def __str__(self):
        return '{}x{}'.format(self.count, self.entry.name)


class Bucket(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        app_label = 'muglaSepetiApp'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("profile"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("company"))
    delivery_note = models.CharField(max_length=500, blank=True, verbose_name=_("delivery note"))
    order_list = models.ManyToManyField(BucketEntry, blank=True, verbose_name=_("order list"))
    order_address = models.CharField(max_length=500, verbose_name=_("order address"))
    order_phone = models.CharField(max_length=500, verbose_name=_("orderer's phone"))
    checked_at = models.DateTimeField(blank=True, null=True, verbose_name=_("check time"))
    ordered_at = models.DateTimeField(blank=True, null=True, verbose_name=_("order time"))
    on_the_way_at = models.DateTimeField(blank=True, null=True, verbose_name=_("on the way time"))
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name=_("deliver time"))
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Cancel time"))
    is_ordered = models.BooleanField(default=False, verbose_name=_("is ordered"))
    is_checked = models.BooleanField(default=False, verbose_name=_("is checked"))
    is_on_the_way = models.BooleanField(default=False, verbose_name=_("is on the way"))
    is_delivered = models.BooleanField(default=False, blank=True, verbose_name=_("is delivered"))
    is_deleted = models.BooleanField(default=False, blank=True, verbose_name=_("is deleted"))

    PAYMENT_OPTIONS = (
        ('N', _("Cash")),
        ('K', _('Credit Card')),
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

    get_borrow.short_description = _('Price')

    def __str__(self):
        return '{} tarihli sipariş'.format(self.ordered_at)


class Comment(models.Model):
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    RATING_LEVELS = (
        ('1', _("Beğenmedim")),
        ('2', _('İdare eder')),
        ('3', _('İyiydi işte')),
        ('4', _('Güzeldi')),
        ('5', _('Mükemmeldi')),
    )
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("owner"))
    bucket = models.OneToOneField(Bucket,
                                  on_delete=models.CASCADE, verbose_name=_("Bucket"))
    rating = models.CharField(max_length=1, choices=RATING_LEVELS)
    comment = models.CharField(max_length=100, verbose_name=_("comment"))
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
