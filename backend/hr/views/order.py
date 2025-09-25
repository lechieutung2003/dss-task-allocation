
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

from base.views import BaseViewSet
from ..models import Order, Assignment, DecisionLog
from ..serializers.order import OrderSerializer, AssignmentSerializer, DecisionLogSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from common.constants.http import Http
from django.db.models import Q

class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_map = {
        "status": "iexact",
        "customer__name": "icontains",
        "note": "icontains",
    }
    
    required_alternate_scopes = {
        "create": [["roles:edit"]],
        "retrieve": [["roles:edit"], ["roles:edit"]],
        "update": [["roles:edit"]],
        "destroy": [["roles:edit"]],
        "list": [["roles:edit"]],
    }
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(preferred_start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(preferred_start_time__lte=end_date)
            
        return queryset
    
    @action(methods=[Http.HTTP_GET], detail=True, url_path="assignments")
    def get_assignments(self, request, pk=None):
        order = self.get_object()
        assignments = Assignment.objects.filter(order=order)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)

class AssignmentViewSet(BaseViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    required_alternate_scopes = {
        "create": [["assignments:edit"]],
        "retrieve": [["assignments:view"], ["assignments:edit"]],
        "update": [["assignments:edit"]],
        "destroy": [["assignments:edit"]],
        "list": [["assignments:view"], ["assignments:edit"]],
    }
