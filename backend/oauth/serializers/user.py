from ..models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "active",
        ]


#Add register
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
User = get_user_model()

# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['email', 'password', 'first_name', 'last_name']

#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             first_name=validated_data.get('first_name', ''),
#             last_name=validated_data.get('last_name', ''),
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Gán quyền mặc định
        from django.contrib.auth.models import Permission
        perm = Permission.objects.get(codename="view_user") # hoặc tên permission phù hợp
        user.user_permissions.add(perm)
        return user