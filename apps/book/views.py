from django.shortcuts import render
from apps.book.models import Book , WishList , Review , Rating , Category , Order , OrderItem
from apps.book.serializers import (BookListSerializer , BookUpdateSerializer , BookCreateSerializer , WishListSerializer , ReviewSerializer , 
                                   RatingSerializer , CategorySerializer , OrderSerializer , OrderItemSerializer)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView , RetrieveAPIView , CreateAPIView , DestroyAPIView , UpdateAPIView 
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser
from rest_framework.exceptions import NotFound , PermissionDenied
from django.db.models import Avg
from django.shortcuts import get_object_or_404



class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    class Meta:
        model = Category
        fields = ['id', 'name']
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()   
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Kategoriyalar ro'yxati",
            'data': response.data  
        }, status=status.HTTP_200_OK)


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = {
            'status': True,
            'msg': "Kitob qo'shildi"
        }
        return Response(data=data , status=status.HTTP_201_CREATED)

class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
def list(self, request, *args, **kwargs):
    response = super().list(request, *args, **kwargs)
    return Response({
        'status': True,
        'msg': "Kitoblar ro'yxati",
        'data': response.data  
    }, status=status.HTTP_200_OK)
class BookDetailView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAdminUser]
    def retrieve(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Kitoblar ro'yxati",
            'data': response.data  
        }, status=status.HTTP_200_OK)
        
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data
        data = {
            'status': True,
            'msg': "Kitob yangilandi"
        }
        return Response(data=data,  status=status.HTTP_200_OK)

class BookDeleteView(DestroyAPIView):
    queryset = Book.objects.all()   
    serializer_class = BookListSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Kitob o'chirildi"
        }, status=status.HTTP_204_NO_CONTENT)

class BookSearchView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [AllowAny]
    search_fields = ['title' , 'author']

    def serch(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data = {
            'status': True,
            'msg': "Kitoblar ro'yxati",
            'data': data
        }
        return Response(data=data, status=status.HTTP_200_OK)
class WishListView(ListAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        data = {
            'status': True,
            'msg': "Sevimlilar ro'yxati",
            'data': data
        }
        return Response(data=data, status=status.HTTP_200_OK)

class WishListCreateView(CreateAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)  # Foydalanuvchini avtomatik bog‘lash
        data = {
            'status': True,
            'msg': "Sevimli kitob qo'shildi"
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

class WishListDeleteView(DestroyAPIView):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [AllowAny]

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        data = response.data
        data = {
            'status': True,
            'msg': "Sevimli kitob o'chirildi"
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

class ReviewCreateView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        existing_review = Review.objects.filter(user=request.user, book_id=book_id).first()

        if existing_review:
            return Response(
                {"status": False, "msg": "Siz allaqachon ushbu kitobga sharh qoldirgansiz"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        data = {
            "status": True,
            "msg": "Review qo'shildi"
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        book_id = self.kwargs.get("book_id") 
        if not Book.objects.filter(id=book_id).exists():  
            raise NotFound(detail="Bunday kitob topilmadi!")  
        
        return Review.objects.filter(book_id=book_id)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {
            'status': True,
            'msg': "Kitobga tegishli sharhlar",
            'data': response.data
        }
        return Response(data=data, status=status.HTTP_200_OK)

class ReviewDeleteView(DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        obj = super().get_object()
        if self.request.user != obj.user and not self.request.user.is_staff:
            raise PermissionDenied("Siz faqat o'z sharhlaringizni o‘chira olasiz!")
        return obj

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Sharh o‘chirildi"
        }, status=status.HTTP_204_NO_CONTENT)

    
class ReviewUpdateView(UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            obj = super().get_object()
        except Review.DoesNotExist:
            raise NotFound("Bunday sharh topilmadi!")
        
        if obj.user != self.request.user:
            raise PermissionDenied("Siz faqat o'z sharhlaringizni yangilashingiz mumkin!")
        
        return obj

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Sharh yangilandi",
            'data': response.data  
        }, status=status.HTTP_200_OK)
    
class ReviewRetrieveView(RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminUser]  # Faqat admin foydalanuvchilar ko‘ra oladi

    def get_object(self):
        try:
            return super().get_object()
        except Review.DoesNotExist:
            raise NotFound("Bunday sharh topilmadi!")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            'status': True,
            'msg': "Sharh ma'lumotlari",
            'data': response.data
        }, status=status.HTTP_200_OK)
    
class RatingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user 
        
        average_rating = Review.objects.filter(user=user).aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        total_rating = Review.objects.filter(user=user).count()

        data = {
            'status': True,
            'msg': "Rating ma'lumotlari",
            'data': {
                'average_rating': round(average_rating, 2),  # Ikkita kasr xonasi bilan
                'total_reviews': total_rating
            }
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
            book_id = request.data.get('book')  # Kitob ID olamiz
            
            # Foydalanuvchi oldin shu kitobga reyting bergan-bermaganligini tekshiramiz
            existing_review = Review.objects.filter(user=request.user, book_id=book_id).first()
            
            if existing_review:
                return Response(
                    {"status": False, "msg": "Siz bu kitobga allaqachon reyting bergansiz."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Agar reyting hali qo‘shilmagan bo‘lsa, uni saqlaymiz
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)

            data = {
                "status": True,
                "msg": "Rating qo'shildi"
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
    def put(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        existing_review = Review.objects.filter(user=request.user, book_id=book_id).first()

        if not existing_review:
            return Response(
                {"status": False, "msg": "Siz hali bu kitobga reyting bermagansiz."},  
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = RatingSerializer(existing_review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response({
            "status": True,
            "msg": "Rating yangilandi"
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        book_id = request.data.get('book')  # Kitob ID olamiz
        existing_review = Review.objects.filter(user=request.user, book_id=book_id).first()

        if not existing_review:
            return Response(
                {"status": False, "msg": "Siz bu kitobga hali reyting bermagansiz."},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_review.delete()

        data = {
            "status": True,
            "msg": "Rating o'chirildi"
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

class OrderCreateView(CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'status': True, 'msg': 'Buyurtma yaratildi'}, status=status.HTTP_201_CREATED)
class UserOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id, user=request.user)

        if order.status in ['shipped', 'delivered']:
            return Response({'status': False, 'msg': 'Bu buyurtmani bekor qilib bo‘lmaydi!'}, status=status.HTTP_400_BAD_REQUEST)

        if order.status == 'cancelled':
            return Response({'status': False, 'msg': 'Buyurtma allaqachon bekor qilingan!'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = 'cancelled'
        order.save()
        
        return Response({'status': True, 'msg': 'Buyurtma bekor qilindi'}, status=status.HTTP_200_OK)
class ChangeOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'status': False, 'msg': 'Noto‘g‘ri status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()

        return Response({'status': True, 'msg': 'Buyurtma statusi yangilandi'}, status=status.HTTP_200_OK)
class OrderHistoryView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')   
