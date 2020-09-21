from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils.safestring import mark_safe
from liststyle import ListStyleAdminMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime
from muglaSepetiApp.models import *
from django import forms

# Register your models here.
# admin.site.register(BucketEntry)
# admin.site.register(Bucket)
admin.site.register(Address)


# admin.site.register(Entry)
# admin.site.register(Company)
# admin.site.register(Profile)


# admin.site.register(FoodGroup)
# admin.site.register(FoodCategory)


# admin.site.register(Menu)

class CustomAdminSite(admin.AdminSite):
    site_title = "Muğla Sepeti"
    site_header = "Muğla Sepeti"
    index_title = "Muğla Sepeti"
    #
    # def each_context(self, request):
    #     context = super().each_context(request)
    #     if request.user.is_authenticated:
    #         try:
    #             comp = Company.objects.get(owner=request.user).slug
    #         except Company.DoesNotExist:
    #             comp = ""
    #
    #         context.update({
    #             'slug': comp
    #         })
    #     return context


customAdminSite = CustomAdminSite()
customAdminSite.register(BucketEntry)
customAdminSite.register(Address)
customAdminSite.register(User, UserAdmin)
customAdminSite.register(Group, GroupAdmin)
customAdminSite.register(Profile)
customAdminSite.register(Comment)
admin.site = customAdminSite


# default admin model for company related views
class DefaultAdminModel(admin.ModelAdmin):
    class Meta:
        abstract = True

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # if user has not multiple companies
            if Company.objects.filter(owner=request.user).count() <= 1:
                if hasattr(obj, 'owner'):
                    obj.owner = request.user
        super(DefaultAdminModel, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DefaultAdminModel, self).get_form(request, obj, **kwargs)
        if 'slug' in form.base_fields:
            form.base_fields['slug'].disabled = True
            form.base_fields['slug'].help_text = _("This field is not editable")
        # if 'owner' in form.base_fields:
        #     form.base_fields['owner'].disabled = True
        #     form.base_fields['owner'].help_text = _("This field is not editable")

        if 'company' in form.base_fields:
            form.base_fields['company'].initial = 1
            if Company.objects.filter(owner=request.user).count() <= 1:
                form.base_fields['company'].disabled = True
                form.base_fields['company'].help_text = _("This field is not editable")

        return form

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(DefaultAdminModel, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'detail':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

    def get_readonly_fields(self, request, obj=None):
        local_read_only_fields = ()
        if obj and not request.user.is_superuser:
            if hasattr(obj, 'owner'):
                local_read_only_fields += ('owner',)
            # if user has not multiple companies
            if Company.objects.filter(owner=request.user).count() <= 1:
                if hasattr(obj, 'company'):
                    local_read_only_fields += ('company',)
        return self.readonly_fields + local_read_only_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            # for extra security
            if db_field.name == "company":
                kwargs["queryset"] = Company.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(DefaultAdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__owner=request.user)


@admin.register(SiteConfig, site=customAdminSite)
class SiteConfigAdmin(DefaultAdminModel):
    pass


@admin.register(Config, site=customAdminSite)
class ConfigAdmin(DefaultAdminModel):
    pass


@admin.register(Company, site=customAdminSite)
class CompanyAdmin(DefaultAdminModel):
    list_display = ('name', 'active_menu', 'open_at', 'close_at', 'get_is_open', 'restaurant_url')
    prepopulated_fields = {'slug': ['name']}

    fields = (
        'owner', 'slug', 'name', 'description', 'logo', 'address', 'active_menu', 'is_open', 'open_at', 'close_at',
        'phone', 'email',
        'instagram',
        'facebook', 'twitter')

    def restaurant_url(self, obj):
        return mark_safe(
            '<a class="button" target="blank_" href="{}">{}</a>'.format(reverse('company_menu', args=[obj.slug]),
                                                                        obj.slug))

    def get_form(self, request, obj=None, **kwargs):
        form = super(CompanyAdmin, self).get_form(request, obj, **kwargs)
        if 'owner' in form.base_fields:
            if obj is not None:
                form.base_fields['owner'].queryset = User.objects.filter(is_staff=True)
        if 'active_menu' in form.base_fields:
            if obj is not None:
                # print(obj.id)
                form.base_fields['active_menu'].queryset = Menu.objects.filter(company__id=obj.id)
        return form

    def get_queryset(self, request):
        qs = super(DefaultAdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Menu, site=customAdminSite)
class MenuAdmin(DefaultAdminModel):
    list_display = ('name', 'count_of_entries')
    # fields = ('name')
    filter_horizontal = ('entry_list',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "entry_list":
                kwargs["queryset"] = Entry.objects.filter(company__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def count_of_entries(self, obj):
        return obj.entry_list.count()
    count_of_entries.short_description = "Ürün Sayısı"


@admin.register(FoodGroup, site=customAdminSite)
class FoodGroupAdmin(DefaultAdminModel):
    list_display = ('name', 'company')


@admin.register(FoodCategory, site=customAdminSite)
class FoodCategoryAdmin(DefaultAdminModel):
    list_display = ('name', 'group', 'company')


@admin.register(Entry, site=customAdminSite)
class EntryAdmin(DefaultAdminModel):
    list_filter = ('company', 'category')
    list_display = ('name', 'detail', 'price', 'company', 'category')


@admin.register(PacketPrice, site=customAdminSite)
class PacketAdmin(DefaultAdminModel):
    list_display = ('name', 'price', 'company')


def make_check(modeladmin, request, queryset):
    for i in queryset.all():
        i.check_order()


def make_on_the_way(modeladmin, request, queryset):
    for i in queryset.all():
        i.order_on_the_way()


def make_delivered(modeladmin, request, queryset):
    for i in queryset.all():
        i.deliver_order()


def make_cancel(modeladmin, request, queryset):
    for i in queryset.all():
        i.cancel_order()


make_check.short_description = _("Mark selected orders as checked")
make_on_the_way.short_description = _("Mark selected orders as on the way")
make_delivered.short_description = _("Mark selected orders as delivered")
make_cancel.short_description = _("Mark selected orders as canceled")


@admin.register(Bucket, site=customAdminSite)
class BucketAdmin(admin.ModelAdmin, ListStyleAdminMixin):
    class Media:
        js = ('admin/js/override_for_change_form.js',)
        css = {
            'all': ('admin/css/override_for_change_form.css',)
        }

    # exclude = ['is_checked', 'is_ordered', 'is_delivered', 'is_on_the_way', 'is_deleted', 'checked_at', 'delivered_at',
    #            'deleted_at', 'on_the_way_at']
    list_display = (
        'get_products', 'get_payment_type', 'delivery_note', 'order_address', 'order_phone', 'get_borrow',
        'get_order_time',
        'status')
    list_filter = ('company',)
    ordering = ['-ordered_at']
    actions = [make_check, make_on_the_way, make_delivered, make_cancel]
    change_list_template = 'admin/change_list_for_bucket.html'

    def get_order_time(self, obj):
        return naturaltime(obj.ordered_at)

    def get_borrow(self, obj):
        return "{}₺".format(floatformat(obj.get_borrow()))

    get_order_time.short_description = _("Order time")
    get_borrow.short_description = _("Borrow")

    def get_row_css(self, obj, index):

        if obj.is_deleted:
            return "red"
        if obj.is_delivered:
            return "green"
        if obj.is_on_the_way:
            return "brown"
        if obj.is_checked:
            return "orange"

        return 'yellow'

    def status(self, obj):
        if obj.is_deleted:
            return _("Canceled")
        elif not obj.is_checked:
            return mark_safe(
                '<a class="btn-chck button" title="{}" name="index" href="{}">{}</a>'.format(
                    _('Mark this order as checked'), reverse('check', args=([obj.pk])), _('Check'))) + mark_safe(
                '<a class="button btn-cancel" title="{}" name="index" href="{}">{}</a>'.format(
                    _('Mark this order as Canceled'), reverse('cancel', args=([obj.pk])), _('Cancel')))
        elif not obj.is_on_the_way:
            return mark_safe(
                '<a class="button btn-prepare" title="{}" name="index" href="{}">{}</a>'.format(
                    _('Mark this order as on the way'), reverse('on_the_way', args=([obj.pk])), _('On the way')))
        elif not obj.is_delivered:
            return mark_safe(
                '<a class="button btn-delivered" title="{}" name="index" href="{}">{}</a>'.format(
                    _('Mark this order as delivered'), reverse('deliver', args=([obj.pk])), _('Delivered')))
        return _("Delivered")

    def get_products(self, obj):
        return mark_safe(
            "</br>".join(["{}x {}".format(p.count, p.entry.name) for p in obj.order_list.all()]))

    get_products.short_description = _("Sipariş Edilen Ürünler")

    def get_queryset(self, request):
        qs = super(BucketAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__owner=request.user, is_ordered=True)

    def changelist_view(self, request, extra_context=None):

        extra_context = {'title': "{}  |  {}".format(_("Muğla Sepeti"), _('Sipariş Paneli'))}

        return super(BucketAdmin, self).changelist_view(request, extra_context=extra_context)
