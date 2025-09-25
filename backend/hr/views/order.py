
from rest_framework import viewsets, permissions
from hr.models.customer import Customer, ServiceType
from hr.models.order import Order
from hr.serializers.order import CustomerSerializer, ServiceTypeSerializer, OrderSerializer
from hr.permissions import IsAdmin, IsEmployee, IsCustomer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        elif hasattr(user, 'role') and user.role == 'employee':
            # Chỉ xem đơn được giao (Assignment)
            return Order.objects.filter(assignment__employee=user)
        elif hasattr(user, 'role') and user.role == 'customer':
            return Order.objects.filter(customer=user)
        return Order.objects.none()

    def get_permissions(self):
        user = self.request.user
        if user.is_staff:
            return [permissions.IsAdminUser()]
        elif hasattr(user, 'role') and user.role == 'employee':
            # Employee chỉ được xem (SAFE_METHODS)
            if self.action in ['list', 'retrieve']:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()]  # Không cho phép các thao tác khác
        elif hasattr(user, 'role') and user.role == 'customer':
            # Customer chỉ được tạo mới, xem đơn của mình
            if self.action in ['list', 'retrieve', 'create']:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAdminUser()]
        return [permissions.IsAdminUser()]
