from django.contrib import admin
from .models import Shop, Tag

class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone_number', 'address_name', 'latitude', 'longitude')
    search_fields = ('name', 'owner__username', 'phone_number', 'address_name')
    list_filter = ('tags',)
    filter_horizontal = ('tags',)

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

admin.site.register(Shop, ShopAdmin)
admin.site.register(Tag, TagAdmin)
