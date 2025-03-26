from django.db import models
from apps.base.models import BaseModel
from apps.user.models import User



class Category(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='book/')
    price = models.PositiveIntegerField()
    


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
    choice = {
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    }
    rating = models.PositiveSmallIntegerField(choices=choice , default=0, null=True)

    def __str__(self):
        return self.rating
    
class WishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlists')

    def __str__(self):
        return self.book
    




