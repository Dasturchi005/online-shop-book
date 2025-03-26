from rest_framework import serializers
from apps.book.models import Book  , Rating , Review , WishList , Category , Order , OrderItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BookCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'image', 'price', 'category']
    
class BookListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Kategoriyani ID o‘rniga to‘liq ma’lumot ko‘rsatish
    average_rating = serializers.SerializerMethodField()  # O‘rtacha reytingni hisoblash

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'image', 'price', 'category', 'average_rating']

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [ 'title', 'author', 'description', 'image', 'price', 'category']
    

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'book', 'rating']

    def validate(self, data):
        if Rating.objects.filter(user=data['user'], book=data['book']).exists():
            raise serializers.ValidationError("Siz ushbu kitobga allaqachon baho bergansiz.")
        return data


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'text']

class WishListSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)  

    class Meta:
        model = WishList
        fields = ['id', 'user', 'book']

class OrderItemSerializer(serializers.ModelSerializer):
    book_title = serializers.ReadOnlyField(source='book.title')  

    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'book_title', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)  # Faqat o‘qish uchun
    total_price = serializers.SerializerMethodField()  # Umumiy narxni qo‘shish

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'items', 'total_price']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.book.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order