from .models import Signal, SignalResult

from rest_framework import serializers


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = '__all__'


class SignalResultSerializer(serializers.ModelSerializer):
    signal = SignalSerializer(required=True)

    class Meta:
        model = SignalResult
        fields = '__all__'

    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     user = User.objects.create_user(
    #         username=user_data['username'],
    #         email=user_data['email'],
    #         password=user_data['password']
    #     )
    #     user_profile = Profile.objects.create(user=user, **validated_data)
    #     return user_profile
