from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from hr.models.order import Order
from hr.serializers.order import OrderSerializer

class SimpleCreateOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
