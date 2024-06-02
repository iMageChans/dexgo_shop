from rest_framework import generics
from .models import Tag, Shop
from .serializers import ShopSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class ShopListCreateView(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]


class ShopSearchView(generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        queryset = Shop.objects.all()
        tags = self.request.query_params.get('tags', None)
        name = self.request.query_params.get('name', None)
        query = self.request.query_params.get('query', None)

        if tags:
            tag_list = tags.split(',')
            queryset = queryset.filter(tags__name__in=tag_list).distinct()

        if name:
            queryset = queryset.filter(name__icontains=name)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(tags__name__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address_name__icontains=query)
            ).distinct()

        return queryset


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
