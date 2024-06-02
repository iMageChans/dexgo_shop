from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_superuser and 'password' in request.data:
            return self.update(request, *args, **kwargs)
        return super().partial_update(request, *args, **kwargs)
