from django.db import models
from django.contrib.auth.models import User
from enum import Enum


class ProfileRole(Enum):
    NoneBotTrader = 1
    Trader = 4
    Analyst = 3
    Admin = 5


profile_role_choices = (
    # (ProfileRole.NoneBotTrader.value, ProfileRole.NoneBotTrader.name),
    (ProfileRole.Trader.value, ProfileRole.Trader.name),
    (ProfileRole.Analyst.value, ProfileRole.Analyst.name)
    # (ProfileRole.Admin.value, ProfileRole.Admin.name)
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, unique=True, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=profile_role_choices, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bot_user_id = models.CharField(max_length=127, null=True, blank=True, unique=True)
    bot_first_name = models.CharField(max_length=127, null=True, blank=True)
    bot_last_name = models.CharField(max_length=127, null=True, blank=True)
    bot_username = models.CharField(max_length=127, null=True, blank=True)
    bot_expected_value = models.CharField(max_length=255, null=True, blank=True)
    bot_future_expected_value = models.CharField(max_length=255, null=True, blank=True)



