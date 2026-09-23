from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductDetailSerializer, CategoryDetailSerializer
)
from .filters import ProductFilter
from .permissions import IsOwnerOrReadOnly, IsReviewAuthorOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadOnly]
    filterset_fields = ['product']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]

    def get_queryset(self):
        if self.action == "retrieve":
            return Category.objects.prefetch_related("products").all()
        return Category.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "in_stock"]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        base_queryset = Product.objects.select_related("category")
        if self.action == "retrieve":
            return base_queryset.annotate(average_rating=Avg("reviews__rating")).prefetch_related("reviews").order_by("-created_at")
        return base_queryset.annotate(average_rating=Avg("reviews__rating")).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer
