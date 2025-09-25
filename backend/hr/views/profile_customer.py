from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hr.serializers.customer import CustomerProfileSerializer

class CustomerProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer = getattr(request.user, "hr_customer", None)
        if not customer:
            return Response({"detail": "Customer not found"}, status=404)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data)
