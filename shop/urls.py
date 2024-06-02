from django.urls import path
from .views import ShopListCreateView, ShopDetailView, ShopSearchView, TagListCreateView, TagDetailView

urlpatterns = [
    path('shops/', ShopListCreateView.as_view(), name='shop-list-create'),
    path('shops/<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    path('shops/search/', ShopSearchView.as_view(), name='shop-search'),
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>/', TagDetailView.as_view(), name='tag-detail'),
]
