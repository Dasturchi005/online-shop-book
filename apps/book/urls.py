from django.urls import path
from apps.book.views import (BookCreateView , BookListView , BookDetailView , BookUpdateView , BookDeleteView , BookSearchView, 
                             CategoryCreateView , WishListCreateView , WishListView  , WishListDeleteView  , ReviewCreateView , 
                             ReviewListView , ReviewDeleteView , RatingView )

urlpatterns = [
    path('create/', BookCreateView.as_view(), name='create'),
    path('list/', BookListView.as_view(), name='list'),
    path('detail/<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='delete'),
    path('search/', BookSearchView.as_view(), name='search'),
    path('category/', CategoryCreateView.as_view(), name='category'),
    path('wishlist/', WishListCreateView.as_view(), name='wishlist'),
    path('wishlists/', WishListView.as_view(), name='wishlists'),
    path('wishlist/delete/<int:pk>/', WishListDeleteView.as_view(), name='wishlist_delete'),
    path('review/', ReviewCreateView.as_view(), name='review'),
    path('reviews/', ReviewListView.as_view(), name='reviews'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('rating/', RatingView.as_view(), name='rating'),   
    
]