from rest_framework import serializers
from accounts.models import UserProfile


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("user","profile_picture","cover_photo","address","country","state","city","pin_code","latitude","longitude","created_at","modified_at")