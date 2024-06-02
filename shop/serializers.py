from rest_framework import serializers
from .models import Shop, Tag

class TagSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'parent', 'children')

class ShopSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Shop
        fields = ('id', 'owner', 'name', 'description', 'phone_number', 'address_name', 'latitude', 'longitude', 'tags')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        shop = Shop.objects.create(**validated_data)
        for tag_data in tags_data:
            tag_name = tag_data.get('name')
            tag, created = Tag.objects.get_or_create(name=tag_name)
            shop.tags.add(tag)
        return shop

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address_name = validated_data.get('address_name', instance.address_name)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag_name = tag_data.get('name')
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance
