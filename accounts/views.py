from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import ChangePasswordSerializer, LoginSerializer, UpdateUserSerializer, UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration view.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        """
        Post request to register a user
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "User": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """
    Client login endpoint.
    """

    serializer_class = LoginSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    A view to change the password of a user.
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    """
    An endpoint to update the profile of a logged-in user
    """

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer
