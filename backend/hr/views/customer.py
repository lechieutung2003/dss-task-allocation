from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hr.serializers.full_user import FullUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from hr.serializers.register_customer import RegisterCustomerSerializer
from rest_framework.permissions import AllowAny
from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from hr.models.order import Order
from hr.serializers.order import OrderSerializer

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = FullUserSerializer(user)
        return Response(serializer.data)


class RegisterCustomerAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response(serializer.to_representation(customer), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

