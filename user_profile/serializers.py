from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Profile

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

class UserProfileSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'groups')

    def get_groups(self, obj):
        user = obj.user
        groups = user.groups.all()
        return GroupSerializer(groups, many=True).data

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()
    groups = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'profile', 'groups')
        read_only_fields = ('username', 'email', 'groups')

    def get_groups(self, obj):
        groups = obj.groups.all()
        return GroupSerializer(groups, many=True).data

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.address = profile_data.get('address', profile.address)
        profile.save()

        return instance
