from rest_framework import serializers
from .models import Userverification
class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Userverification
        fields=('__all__');

