from django.contrib import admin
from muglaSepetiApp.models import *

# Register your models here.
admin.site.register(BucketEntry)
admin.site.register(Bucket)
admin.site.register(Address)
admin.site.register(Entry)
# admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(FoodGroup)
admin.site.register(FoodCategory)
admin.site.register(Menu)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_is_open')
    # fields = ('__all__',)
