from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('', views.Signals)
# router.register('result', views.SignalResults)


urlpatterns = [
    path('', views.Signals.as_view()),
    path('result/', views.SignalResults.as_view())
]
