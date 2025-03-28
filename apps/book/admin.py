from django.contrib import admin
from .models import Book , WishList , Review , Rating , Category , Order , OrderItem

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title' , 'author' , 'id',  'price']
    search_fields = ['title' , 'author']
admin.site.register(WishList)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)