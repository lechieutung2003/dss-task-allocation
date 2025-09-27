from hr.models import Employee, Assignment
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from hr.serializers import AssignmentSerializer

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
