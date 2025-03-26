from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated , IsAdminUser 
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status  
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, UserLoginSerializer, UserProfileSerializer, UserUpdateSerializer


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    data = {
        'status': True,
        'msg': "Ro'yxatdan o'tdingiz"
    }

class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
    
    data = {
        'status': True,
        'msg': "Login qilindi"
    }
       

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    data = {
        'status': True,
        'msg': "Logout qilindi"
    }

class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    data = {
        'status': True,
        'msg': "Profil ma'lumotlari"
    }
    


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        data = {
            'status': True,
            'msg': "Profil yangilandi"
        }
        return Response(data=data)



class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        data = {
            'status': True,
            'msg': "Profil o'chirildi"
        }
        return Response(data=data)

class UserListView(ListAPIView):
    queryset = User.objects.all()    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
