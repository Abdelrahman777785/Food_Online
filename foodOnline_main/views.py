from django.shortcuts import render
from django.http import HttpResponse

from vendor.models import Vendor
from accounts.models import User 

def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count = vendors.count()

    # Show in html in home page
    vendors_show = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count_show = vendors_show.count()
    user_count_show = User.objects.filter(is_active=True)
    user_count_show = user_count_show.count()

    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
        'user_count_show':user_count_show,
        'vendor_count_show':vendor_count_show,
    }
    return render(request, 'home.html', context)


