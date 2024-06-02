from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'inviter', 'invite_code', 'phone_number', 'address')
    search_fields = ('user__username', 'inviter__username', 'invite_code')
    list_filter = ('inviter',)

admin.site.register(Profile, ProfileAdmin)
