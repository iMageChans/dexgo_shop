import uuid

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, EmptySerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        userGroup = Group.objects.get(name=response.data['user'])
        user.groups.add(userGroup)
        response.data['refresh'] = str(refresh)
        response.data['access'] = str(refresh.access_token)
        return response


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user_serializer.data,
        }, status=status.HTTP_200_OK)


class GenerateInviteCodeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        if not profile.invite_code:
            profile.invite_code = str(uuid.uuid4())[:10]
            profile.save()
        return Response({'invite_code': profile.invite_code}, status=status.HTTP_200_OK)


class ShareInviteCodeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile
        return Response({'invite_code': profile.invite_code}, status=status.HTTP_200_OK)
