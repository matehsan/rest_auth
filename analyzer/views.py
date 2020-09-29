from django.contrib.auth.models import User

from rest_framework import status as s

from .models import Profile
from rest_framework import generics

from . import serializers
from . import permissions


def send_email(email):
    print(email)


class Analyzer(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        res = super().create(request, *args, **kwargs)
        send_email(request.data['user.email'])
        res.status_code = s.HTTP_201_CREATED
        return res
