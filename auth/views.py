from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings

from . import serializers
from . import permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """create and update user"""
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)


class UserLoginApiView(ObtainAuthToken):
    """create user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
