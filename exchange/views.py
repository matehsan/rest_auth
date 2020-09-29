from rest_framework import generics

from .models import Signal, SignalResult
from . import permissions, serializers


class Signals(generics.ListAPIView):
    queryset = Signal.objects.all()
    serializer_class = serializers.SignalSerializer
    permission_classes = []


class SignalResults(generics.ListAPIView):
    queryset = SignalResult.objects.filter(signal__creator_profile__user_id=13)
    serializer_class = serializers.SignalResultSerializer
    permission_classes = []
