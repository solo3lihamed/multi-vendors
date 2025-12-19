from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from .models import VendorProfile

User = get_user_model()

class VendorRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    store_name = forms.CharField(max_length=255)
    
    class Meta:
        model = VendorProfile
        fields = ['store_name', 'description']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm
    
    def save(self, commit=True):
        # Create User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            role=User.Roles.VENDOR
        )
        # Create Vendor Profile
        vendor = super().save(commit=False)
        vendor.user = user
        vendor.slug = slugify(vendor.store_name, allow_unicode=True)
        
        # Ensure unique slug (simple version)
        if VendorProfile.objects.filter(slug=vendor.slug).exists():
            vendor.slug = f"{vendor.slug}-{user.id}"
            
        if commit:
            vendor.save()
        return vendor
