from django.contrib import admin
from .models import VendorProfile

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'user', 'is_subscribed', 'slug')
    list_filter = ('is_subscribed',)
    search_fields = ('store_name', 'user__username')
    prepopulated_fields = {'slug': ('store_name',)}
