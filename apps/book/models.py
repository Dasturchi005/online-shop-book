from django.db import models
from apps.base.models import BaseModel
from apps.user.models import User



class Category(BaseModel):
    name = models.CharField(max_length=255 , unique=True)

    def __str__(self):
        return self.name
class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='book/')
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="books")


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
    
class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    def __str__(self):
        return self.text

class Rating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=0)

    def __str__(self):
        return f"{self.rating} - {self.book.title}"

    class Meta:
        unique_together = ('user', 'book')

class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    

class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    @property
    def total_price(self):
        return sum(item.book.price * item.quantity for item in self.items.all())

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Necha dona olgan

    def __str__(self):
        return f"{self.quantity} x {self.book.title} (Order {self.order.id})"



