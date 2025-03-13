from django.http import JsonResponse

from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializers

def UserProfil_get(request):
    userprofile = UserProfileSerializers(
        UserProfile.objects.all().order_by("id"),
        many=True
    ).data 

    return JsonResponse({"userprofile": userprofile})  # Return the data as JSON