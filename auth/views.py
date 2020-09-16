from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework import permissions

from . import serializers
from . import permissions as p


# /create
class CreateUser(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 200,
            'message': 'User successfully created',
            'data': response.data
        })


# /user
class UserProfile(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)


# /user/password
class PasswordUpdate(generics.UpdateAPIView):
    model = User

    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, p.UpdateOwnProfile)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /login
class UserLoginApiView(ObtainAuthToken):
    """create user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
