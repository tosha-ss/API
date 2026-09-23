from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9]+(?:-[a-z0-9]+)*$',
                message="Slug должен содержать только латинские буквы в нижнем регистре, цифры и дефисы."
            )
        ]
    )

    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    owner = serializers.ReadOnlyField(source="owner.username")
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category_name', 'name', 'description', 'price', 'in_stock', 'created_at', 'category', 'owner', 'average_rating']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

    def validate_in_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Количество на складе не может быть отрицательным.")
        return value

    def validate(self, data):
        if len(data.get('name', '')) < 2:
            raise serializers.ValidationError({"name": "Название товара должно содержать хотя бы 2 символа."})
        return data

    def get_average_rating(self, obj) -> float | None:
        annotated_rating = getattr(obj, "average_rating", None)
        if annotated_rating is not None:
            return round(annotated_rating, 1)
        from django.db.models import Avg
        result = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(result, 1) if result else None

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'comment', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть строго от 1 до 5.")
        return value

class ProductDetailSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['reviews']

class CategoryDetailSerializer(CategorySerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'created_at', 'products']
