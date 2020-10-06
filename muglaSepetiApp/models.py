import os

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
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
        verbose_name = _("Address")
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
    address = models.ForeignKey(Address, related_name='profile_address', on_delete=models.CASCADE, null=True,
                                verbose_name=_("address"))
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

    def get_bucket(self):
        bucket, _ = self.bucket.get_or_create(is_ordered=False, is_deleted=False)
        if _ is True:
            bucket.profile = self
            bucket.order_address = self.address.location
            bucket.order_phone = self.phone
            bucket.save()
        return bucket

    def get_last_orders(self):
        bucket = self.bucket.filter(is_ordered=True).order_by('-ordered_at')
        return bucket

    def __str__(self):
        return self.user.username


class GetCompanyOpen(models.Manager):
    def get_query_set(self):
        return super(GetCompanyOpen, self).get_query_set().filter(
            open_at__lte=timezone.now().time(), close_at__gt=timezone.now().time())


class Config(models.Model):
    name = models.CharField(max_length=20, null=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True, verbose_name=_("phone number"))
    favicon = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                validators=[FileExtensionValidator(allowed_extensions=['ico'])], verbose_name=_("icon"))

    email = models.CharField(validators=[email_regex], max_length=50, blank=True, verbose_name=_("email address"))
    # mail_before_text = models.CharField(max_length=500, blank=True, verbose_name=_("password reset text head"))
    # mail_after_text = models.CharField(max_length=500, blank=True, verbose_name=_("password reset text end"))
    address = models.CharField(max_length=100, null=True, verbose_name=_("address"))
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_("Site Logo"))
    footer_logo = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_("Footer Logo"))
    site_description = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("Site Description"))
    content_description = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("Content Description"))
    slider_title = models.CharField(max_length=20, blank=True, null=True, verbose_name=_("Slider Title"))
    slider_description = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Slider Description"))
    slider_image_1 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                       verbose_name=_("Slider Image 1"))
    slider_image_2 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                       verbose_name=_("Slider Image 2"))
    slider_image_3 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                       verbose_name=_("Slider Image 3"))
    slider_image_4 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                       verbose_name=_("Slider Image 4"))
    menu_background = models.ImageField(upload_to=get_image_path,
                                        validators=[FileExtensionValidator(allowed_extensions=['png'])], blank=True,
                                        null=True,
                                        verbose_name=_("Menu Background"))
    menu_inner_background = models.ImageField(upload_to=get_image_path,
                                              validators=[FileExtensionValidator(allowed_extensions=['png'])],
                                              blank=True,
                                              null=True,
                                              verbose_name=_("Menu Inner Background"))
    bread_crumb_background = models.ImageField(upload_to=get_image_path,
                                               blank=True, null=True,
                                               verbose_name=_("Breadcrumb Background"))

    order_background = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                         validators=[FileExtensionValidator(allowed_extensions=['png'])],
                                         verbose_name=_("Order Background"))
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    googleplus = models.URLField(blank=True, null=True)

    about_title = models.CharField(max_length=50, blank=True, null=True)
    about_description = models.CharField(max_length=1500, blank=True, null=True)
    about_image_1 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                      verbose_name=_("About Image 1"))
    about_image_2 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                      verbose_name=_("About Image 2"))
    about_image_3 = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                      verbose_name=_("About Image 3"))
    about_image_large = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                          verbose_name=_("About Image Large"))
    about_background_quotes = models.ImageField(upload_to=get_image_path, blank=True, null=True,
                                                verbose_name=_("About Quotes Background "))
    about_fact_title_1 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Statistic Title 1"))
    about_fact_value_1 = models.IntegerField(null=True, blank=True, verbose_name=_("Statistic Value 1"))
    about_fact_title_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Statistic Title 2"))
    about_fact_value_2 = models.IntegerField(null=True, blank=True, verbose_name=_("Statistic Value 2"))
    about_fact_title_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Statistic Title 3"))
    about_fact_value_3 = models.IntegerField(null=True, blank=True, verbose_name=_("Statistic Value 3"))
    about_fact_title_4 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Statistic Title 4"))
    about_fact_value_4 = models.IntegerField(null=True, blank=True, verbose_name=_("Statistic Value 4"))

    about_content_title = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Content Title"))
    about_content_description = models.CharField(max_length=500, null=True, blank=True,
                                                 verbose_name=_("Content Description"))

    about_info_title_1 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Information Title 1"))
    about_info_description_1 = models.CharField(max_length=150, null=True, blank=True,
                                                verbose_name=_("Information Description 1"))
    about_info_title_2 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Information Title 2"))
    about_info_description_2 = models.CharField(max_length=150, null=True, blank=True,
                                                verbose_name=_("Information Description 2"))
    about_info_title_3 = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Information Title 3"))
    about_info_description_3 = models.CharField(max_length=150, null=True, blank=True,
                                                verbose_name=_("Information Description 3"))
    about_quote_title = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Quotes Title"))
    about_quote_1 = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("Quote 1"),
                                     help_text=_("Type writer name end of the text heading with '-' Ex:-Furkankykc"))
    about_quote_2 = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("Quote 2"),
                                     help_text=_("Type writer name end of the text heading with '-' Ex:-Furkankykc"))
    about_quote_3 = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("Quote 3"),
                                     help_text=_("Type writer name end of the text heading with '-' Ex:-Furkankykc"))

    def __str__(self):
        return self.name


class SiteConfig(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("Name"))
    config = models.ForeignKey(Config, on_delete=models.SET_NULL, null=True, verbose_name=_("Site Config"))

    def __str__(self):
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_("owner"))
    name = models.CharField(max_length=20, verbose_name=_("name"))
    description = models.CharField(max_length=500, verbose_name=_("description"))
    logo = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_("logo"))
    slug = models.SlugField(blank=True, verbose_name=_("slug"))
    active_menu = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='comp_active_menu', verbose_name=_("active menu"))
    service_delay = models.DurationField(verbose_name=_("Service Delay"))
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,
                             null=True, verbose_name=_("phone number"))
    email = models.CharField(validators=[email_regex], max_length=50, blank=True, verbose_name=_("email adress"))
    address = models.CharField(max_length=500, verbose_name=_("address"))
    open_at = models.TimeField(default=timezone.now, verbose_name=_("open time"))
    close_at = models.TimeField(default=timezone.now, verbose_name=_("close time"))
    is_open = models.BooleanField(default=False, verbose_name=_("is Open"), help_text=_(
        "if this box not checked your company wont open even if it currently open-hours"))
    is_busy = models.BooleanField(default=False, verbose_name=_("is Busy"), help_text=_(
        "if this box is checked your company status will be changed to busy which mean you might not be able to send packet to buyer on right time"))
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

        return (x for x in cls.objects.all() if x.get_is_open)

    def get_is_open(self):
        current_time = timezone.localtime(timezone.now()).time()
        if self.is_open:
            if self.open_at > self.close_at:
                return self.open_at < current_time > self.close_at
            else:
                return self.open_at < current_time < self.close_at

        return False

    def get_comments(self):
        return Bucket.objects.filter(company=self).order_by('-comment__time')

    def get_rating(self):
        rating = Bucket.objects.filter(company=self).aggregate(Avg('comment__rating'))['comment__rating__avg']
        return rating

    def get_packet_prices(self):
        return PacketPrice.objects.filter(company=self)

    get_is_open.short_description = _("Şuanda Açık mı?")

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
    collation = models.ForeignKey('CollationList', on_delete=models.CASCADE, blank=True, null=True,
                                  verbose_name=_('collation'))
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True, verbose_name=_('product image'))
    is_disabled = models.BooleanField(default=False, verbose_name=_('Hide product'), help_text=_(
        'if your product is out of stack select this option to hide from products'))
    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, verbose_name=_('category'))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_entry', verbose_name=_('company'))

    @property
    def get_image(self):
        return self.image or self.category.image

    def get_food_rating(self):
        comment_ratings = self.get_comments().aggregate(Avg('rating'))['rating__avg'] or 0

        return int(comment_ratings)

    def __str__(self):
        return self.name

    def get_comments(self):
        return Comment.objects.filter(bucket__order_list__entry_id=self.id).order_by('-time')


class Menu(models.Model):
    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _("Menus")

    name = models.CharField(max_length=50, verbose_name=_("Name"))
    entry_list = models.ManyToManyField(Entry, verbose_name=_("Entry list"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Company"))

    def __str__(self):
        return self.name


class BucketEntry(models.Model):
    class Meta:
        verbose_name = _("Bucket Product")
        verbose_name_plural = _("Bucket Products")

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, verbose_name=_("Product"))
    # ara toplam olmadan gereksiz
    price = models.FloatField(default=0, verbose_name=_("Total Bucket Price"))
    collation = models.ForeignKey('BucketCollation', on_delete=models.CASCADE, null=True, blank=True)
    count = models.IntegerField(default=1, verbose_name=_("Count"))

    def set_collation(self, collation):
        self.collation = collation

    ##todo burdan  sonrasını bağlamadım  price ye ekliyor bırakıyor aparatif form u hazırlayıp her aperatifi olan bucket entry icin eklemek lazım
    def calc_price(self):
        self.price = self.collation.calculate_extra_price()

    def __str__(self):
        return '{}x{}'.format(self.count, self.entry.name)


class PacketPrice(models.Model):
    class Meta:
        verbose_name = _("Minimum Packet Price")
        verbose_name_plural = _("Minimum Packet Prices")

    name = models.CharField(max_length=50, verbose_name=_("Address"))
    price = models.FloatField(default=5, verbose_name=_("Minimum Price"))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("Company"))

    def __str__(self):
        return self.name


class Bucket(models.Model):
    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        app_label = 'muglaSepetiApp'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("profile"), related_name='bucket')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name=_("company"), null=True, blank=True)
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

    def set_address(self):
        self.order_address = self.profile.address.location
        self.save()

    def set_phone(self):
        self.order_phone = self.profile.phone
        self.save()

    def set_profile(self, profile):
        self.profile = profile
        self.save()

    def order(self, profile: Profile):
        self.is_ordered = True
        self.ordered_at = timezone.localtime(timezone.now())
        self.set_profile(profile)
        self.set_phone()
        self.set_address()
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

        if _:
            self.company = obj.entry.company
            obj.count = count
            obj.price = entry.price
            obj.entry = entry
        else:
            obj.count = obj.count + count
            if self.company != entry.company:
                return ValidationError

        obj.save()
        self.save()

    def get_borrow(self):
        item_sum = Sum(F('price') * F('count'), output_field=models.FloatField())
        borrow = self.order_list.aggregate(amount=item_sum, ).get('amount', 0)
        return borrow

    def get_payment_type(self):
        if self.payment_type:
            return dict(self.PAYMENT_OPTIONS)[self.payment_type]
        return None

    get_borrow.short_description = _('Price')
    get_payment_type.short_description = _('Payment Type')

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
    comment = models.CharField(max_length=100, null=True, blank=True,
                               verbose_name=_("comment"))
    time = models.DateTimeField(auto_now_add=True)

    def get_rating_value(self):
        if self.rating:
            return int(self.rating)
        else:
            return 0

    def __str__(self):
        return self.comment


class Annoucment(models.Model):
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    message = models.CharField(max_length=250, verbose_name=_("Message"))
    is_active = models.BooleanField(default=True, verbose_name=("is annoucment active"))


class Collation(models.Model):
    name = models.CharField(max_length=40, verbose_name=_('Name'))
    price = models.FloatField(verbose_name=_('Price'))

    def __str__(self):
        return self.name


class CollationNode(models.Model):
    collation = models.ForeignKey(Collation, on_delete=models.CASCADE, verbose_name=_('Collation'))
    is_already_added = models.BooleanField(default=False,
                                           verbose_name=_('is this material already in your food menu price'))

    def __str__(self):
        return f'{self.collation.name} , {self.is_already_added}'


class CollationList(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('name'))
    collation_list = models.ManyToManyField(CollationNode, verbose_name=_('Collation List'))

    def get_extras(self):
        return self.collation_list.filter(is_already_added=False)

    def get_status(self, col_ids: list):
        col_list = self.collation_list.filter(collation_id__in=col_ids)
        final_string = ""
        for col in col_list:
            final_string += f'{col.collation.name}: '
            if col.is_already_added:
                final_string += f'Olmasın\n'
            else:
                final_string += f'Extra istiyorum\n'

    def __str__(self):
        return self.name


class BucketCollation(models.Model):
    collation = models.ForeignKey(CollationList, on_delete=models.CASCADE)
    collation_list = models.ManyToManyField(CollationNode, verbose_name=_('Collation List'))

    def calculate_extra_price(self):
        return self.collation.get_extras().filter(
            collation_id__in=self.collation_list.filter(is_already_added=True).values_list('pk', flat=True)).aggregate(
            Sum('collation__price'))['collation__price__sum']
