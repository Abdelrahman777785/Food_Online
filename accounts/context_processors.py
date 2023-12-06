from vendor.models import Vendor
from django.conf import settings

def get_vendor(request):
    try:
        vendor = Vendor.objects.get(user=request.user)
    except:
        vendor = None
    return dict(vendor=vendor)


# def get_google_api(request):
#     return {'MAPQUEST_API_KEY': settings.MAPQUEST_API_KEY}