from django.db import models
from django.conf import settings

class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField(blank=True)
    
    # Billing/SaaS stuff (dummy)
    is_subscribed = models.BooleanField(default=False) 

    def __str__(self):
        return self.store_name
