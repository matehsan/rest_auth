from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register('profile', views.UserProfileViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('user/', views.UserProfile.as_view()),
    path('create/', views.CreateUser.as_view()),
    path('user/password/', views.PasswordUpdate.as_view()),

    # path('', include(router.urls))
]
