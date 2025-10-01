from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer
from hr.models.order import Order
from hr.serializers.order import OrderSerializer
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

class SimpleCreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerOrdersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        from hr.models import Order
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        orders = Order.objects.filter(customer=customer)
        from hr.serializers.order import OrderSerializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class UpdateOrderFeedbackAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, order_id):
        user_id = getattr(request.user, "id", None)
        if not user_id:
            return Response({"detail": "Không xác định được user"}, status=403)

        from hr.models.customer import Customer
        try:
            customer = Customer.objects.get(user_id=user_id)
        except Customer.DoesNotExist:
            return Response({"detail": "User không phải là customer"}, status=403)

        try:
            order = Order.objects.get(id=order_id, customer=customer)
        except Order.DoesNotExist:
            return Response({"detail": "Không tìm thấy đơn hàng"}, status=404)

        # Chỉ cho phép cập nhật feedback cho đơn hàng đã hoàn thành
        if order.status != 'completed':
            return Response({
                "detail": "Chỉ có thể gửi phản hồi cho đơn hàng đã hoàn thành"
            }, status=400)

        customer_feedback = request.data.get('customer_feedback', '')
        if not customer_feedback.strip():
            return Response({"detail": "Phản hồi không được để trống"}, status=400)

        order.customer_feedback = customer_feedback.strip()
        order.save()

        from hr.serializers.order import OrderSerializer
        serializer = OrderSerializer(order)
        return Response(serializer.data)