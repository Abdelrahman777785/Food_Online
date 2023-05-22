from django.shortcuts import render, get_object_or_404
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from .forms import VendorForm


def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    profile_form = UserProfileForm(instance = profile)
    vendor_form = VendorForm(instance = vendor)

    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'vendor': vendor,
        'profile': profile,
    }
    return render(request, 'vendor/vprofile.html', context)
