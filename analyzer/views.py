from django.contrib.auth.models import User

from .models import Profile
from rest_framework import generics


from . import serializers
from . import permissions


class Analyzer(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = []
