from django.contrib.auth import authenticate 
from rest_framework import serializers
from apps.user.models import User  

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'password': 'Parollar mos emas'})
        return attrs

    def create(self, validated_data):
        
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, email):

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Ushbu email allaqachon ishlatilgan.")
        return email

    def validate_username(self, username):
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Ushbu username allaqachon ishlatilgan.")
        return username
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'first_name', 'last_name']
