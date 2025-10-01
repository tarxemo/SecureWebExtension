from rest_framework import serializers
from .models import RestrictedURL

class RestrictedURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestrictedURL
        fields = ['url']
