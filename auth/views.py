from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework import permissions
from rest_framework.views import APIView

from . import serializers
from . import permissions as p


# /create
class CreateUser(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            'status': 201,
            'message': 'User successfully created',
            'data': response.data
        }, status.HTTP_201_CREATED)


# /user
class UserProfile(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)


# /user/password
class PasswordUpdate(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, p.UpdateOwnProfile)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = serializers.ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /login
class UserLoginApiView(ObtainAuthToken):
    """create user authentication token"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
