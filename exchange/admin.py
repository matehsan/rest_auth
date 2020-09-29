from django.contrib import admin
from .models import Signal, SignalResult

admin.site.register(Signal)
admin.site.register(SignalResult)
