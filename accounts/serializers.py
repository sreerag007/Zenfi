from .models import User
from rest_framework import serializers
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests as google_requests

class GoogleSignUpSerializer(serializers.Serializer):
    id_token=serializers.CharField()

    def validate(self, attrs):
        try:
            google_user=id_token.verify_oauth2_token(
                attrs['id_token'],
                google_requests.Request()
            )
            if google_user['aud'] not in settings.GOOGLE_CLIENT_ID:
                raise serializers.ValidationError("Invalid Audience")

        except ValueError as e:
            raise serializers.ValidationError("Invalid Google Token")

        attrs['google_user']=google_user

        return attrs

class ProfileCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'id','profile_picture'
        ]        

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'id','full_name','profile_picture'
        ]        

class UserDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            'id','full_name'
        ]        