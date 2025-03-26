from rest_framework import serializers
from apps.book.models import Book  , Rating , Review , WishList , Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'image', 'price', 'category']
    
class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'image', 'price'  , 'category' , 'rating' ]

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'description', 'image', 'price', 'category']
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'rating']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'text']

class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ['id', 'user', 'book']