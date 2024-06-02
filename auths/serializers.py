from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from user_profile.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    invite_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'invite_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        invite_code = validated_data.pop('invite_code', None)
        user = User.objects.create_user(**validated_data)
        if invite_code:
            try:
                inviter_profile = Profile.objects.get(invite_code=invite_code)
                user.profile.inviter = inviter_profile.user
                user.profile.save()
            except Profile.DoesNotExist:
                pass
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class EmptySerializer(serializers.Serializer):
    pass
