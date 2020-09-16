from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    # def create(self, validated_data):
    #     """Create and return a new user"""
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         password=validated_data['password']
    #     )
    #
    #     return user

    # def update(self, instance, validated_data):
    #
    #     if 'username' in validated_data:
    #         instance.username = validated_data['username']
    #     if 'email' in validated_data:
    #         instance.email = validated_data['email']
    #     if 'password' in validated_data:
    #         instance.password = make_password(validated_data['password'])
    #     instance.save()
    #     return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # fields = '__all__'
        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'}
            }
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True, write_only=True,
                                         style={'input_type': 'password', 'placeholder': 'Old Password'})
    new_password = serializers.CharField(required=True, write_only=True,
                                         style={'input_type': 'password', 'placeholder': 'New Password'})
