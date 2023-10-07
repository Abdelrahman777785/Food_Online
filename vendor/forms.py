from django import forms
from .models import Vendor 
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'upload-btn foodbakery-dev-cover-upload-btn', 'style':'display:;'}), validators=[allow_only_images_validator])  # style button my restaurant

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
