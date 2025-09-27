from rest_framework import viewsets
from base.views import BaseViewSet
from rest_framework import permissions
from ..models import Order, Assignment, DecisionLog
from ..models.customer import Customer, ServiceType
from ..serializers.order import (
    OrderSerializer, AssignmentSerializer, DecisionLogSerializer,
    CustomerSerializer, ServiceTypeSerializer
)
from rest_framework.decorators import action
from rest_framework.response import Response
from common.constants.http import Http
from django.db.models import Q
from hr.permissions import IsAdmin, IsEmployee, IsCustomer

class OrderViewSet(BaseViewSet):
    # API lấy chi tiết đơn hàng theo id
    @action(methods=[Http.HTTP_GET], detail=True, url_path="detail")
    def detail(self, request, pk=None):
        order = self.get_object()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    search_map = {
        "status": "iexact",
        "customer__name": "icontains",
        "note": "icontains",
    }
    required_alternate_scopes = {
    "create": [["roles:edit"]],
    "retrieve": [["roles:edit"], ["roles:view"]],
    "update": [["roles:edit"]],
    "destroy": [["roles:edit"]],
    "list": [["roles:edit"], ["roles:view"]],
    "get_assignments": [["roles:edit"], ["roles:view"]],
}

    def get_queryset(self):
        queryset = super().get_queryset()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(preferred_start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(preferred_start_time__lte=end_date)
        user = self.request.user
        if user.is_staff:
            return queryset
        elif hasattr(user, 'role') and user.role == 'employee':
            return queryset.filter(assignment__employee=user)
        elif hasattr(user, 'role') and user.role in ['customer', 'guest']:
            return queryset.filter(customer=user)
        return queryset.none()

    def get_permissions(self):
        user = self.request.user
        if user.is_staff:
            return [permissions.IsAdminUser()]
        elif hasattr(user, 'role'):
            if user.role == 'employee':
                if self.action in ['list', 'retrieve', 'get_assignments']:
                    return [permissions.IsAuthenticated(), IsEmployee()]
                return [permissions.IsAdminUser()]
            elif user.role in ['customer', 'guest']:
                # Customer/guest được tạo đơn, xem đơn của mình
                if self.action in ['list', 'retrieve', 'create']:
                    return [permissions.IsAuthenticated(), IsCustomer()]
                return [permissions.IsAdminUser()]
        return super().get_permissions()

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

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    def get_permissions(self):
        if self.request.user and self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all().order_by('id')
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]