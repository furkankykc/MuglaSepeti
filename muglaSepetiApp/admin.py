from django.contrib import admin

from muglaSepetiApp.models import *

# Register your models here.
admin.site.register(BucketEntry)
# admin.site.register(Bucket)
admin.site.register(Address)
# admin.site.register(Entry)
# admin.site.register(Company)
admin.site.register(Profile)


# admin.site.register(FoodGroup)
# admin.site.register(FoodCategory)


# admin.site.register(Menu)

# default admin model for company releated views
class DefaultAdminModel(admin.ModelAdmin):
    class Meta:
        abstract = True

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # if user has not multiple companies
            if Company.objects.filter(owner=request.user).count() <= 1:
                obj.owner = request.user
        super(DefaultAdminModel, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super(DefaultAdminModel, self).get_form(request, obj, **kwargs)
        if 'slug' in form.base_fields:
            form.base_fields['slug'].disabled = True
            form.base_fields['slug'].help_text = "This field is not editable"
        # if 'owner' in form.base_fields:
        #     form.base_fields['owner'].disabled = True
        #     form.base_fields['owner'].help_text = "This field is not editable"

        return form

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


@admin.register(Company)
class CompanyAdmin(DefaultAdminModel):
    list_display = ('name', 'active_menu', 'open_at', 'close_at', 'is_currently_open')
    prepopulated_fields = {'slug': ['name']}

    fields = (
        'owner', 'slug', 'name', 'logo', 'address', 'active_menu', 'is_open', 'open_at', 'close_at', 'phone', 'email',
        'instagram',
        'facebook', 'twitter')

    @staticmethod
    def is_currently_open(obj):
        return obj.get_is_open()

    def get_form(self, request, obj=None, **kwargs):
        form = super(DefaultAdminModel, self).get_form(request, obj, **kwargs)
        if 'active_menu' in form.base_fields:
            if obj is not None:
                print(obj.id)
                form.base_fields['active_menu'].queryset = Menu.objects.filter(company__id=obj.id)
        return form

    def get_queryset(self, request):
        qs = super(DefaultAdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(Menu)
class MenuAdmin(DefaultAdminModel):
    list_display = ('name', 'count_of_entries')
    # fields = ('name')
    filter_horizontal = ('entry_list',)

    def count_of_entries(self, obj):
        return obj.entry_list.count()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "entry_list":
                kwargs["queryset"] = Entry.objects.filter(company__owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(FoodGroup)
class FoodGroupAdmin(DefaultAdminModel):
    list_display = ('name', 'company')


@admin.register(FoodCategory)
class FoodCategoryAdmin(DefaultAdminModel):
    list_display = ('name', 'group', 'company')


@admin.register(Entry)
class EntryAdmin(DefaultAdminModel):
    list_filter = ('company', 'category')
    list_display = ('name', 'detail', 'price', 'company', 'category')


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


make_check.short_description = "Mark selected orders as checked"
make_on_the_way.short_description = "Mark selected orders as on the way"
make_delivered.short_description = "Mark selected orders as delivered"
make_cancel.short_description = "Mark selected orders as canceled"


@admin.register(Bucket)
class BucketAdmin(admin.ModelAdmin):
    exclude = ['is_checked', 'is_ordered', 'is_delivered', 'is_on_the_way', 'is_deleted', 'checked_at', 'delivered_at',
               'deleted_at', 'on_the_way_at']
    list_display = ('get_products', 'delivery_note', 'order_address', 'order_phone', 'get_borrow', 'company')
    list_filter = ('company',)
    ordering = ['ordered_at']
    actions = [make_check, make_on_the_way, make_delivered, make_cancel]

    def get_products(self, obj):
        return ",".join([i.name for i in [p.entry for p in obj.order_list.all()]])

    def get_queryset(self, request):
        qs = super(BucketAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__owner=request.user, is_ordered=True)
