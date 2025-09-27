from rest_framework import viewsets, permissions
from ..models import Order, Assignment, DecisionLog
from ..models.customer import Customer, ServiceType
from ..serializers.order import OrderSerializer, AssignmentSerializer, DecisionLogSerializer
from ..serializers.order import CustomerSerializer, ServiceTypeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from common.constants.http import Http
from django.db.models import Q
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

class OrderViewSets(BaseViewSet):
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
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(preferred_start_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(preferred_start_time__lte=end_date)
        
        # Apply role-based filtering
        user = self.request.user
        if user.is_staff:
            # Admin sees all orders
            return queryset
        elif hasattr(user, 'role') and user.role == 'employee':
            # Employee only sees assigned orders
            return queryset.filter(assignment__employee=user)
        elif hasattr(user, 'role') and user.role == 'customer':
            # Customer only sees their orders
            return queryset.filter(customer=user)
        
        return queryset.none()
    
    def get_permissions(self):
        # Override scopes if needed for specific user roles
        user = self.request.user
        if user.is_staff:
            return [permissions.IsAdminUser()]
        elif hasattr(user, 'role'):
            if user.role == 'employee':
                # Employee can only view orders
                if self.action in ['list', 'retrieve', 'get_assignments']:
                    return [permissions.IsAuthenticated(), IsEmployee()]
                return [permissions.IsAdminUser()]
            elif user.role == 'customer':
                # Customer can view and create orders
                if self.action in ['list', 'retrieve', 'create']:
                    return [permissions.IsAuthenticated(), IsCustomer()]
                return [permissions.IsAdminUser()]
        
        # Use default scopes from BaseViewSet
        return super().get_permissions()
    
    @action(methods=[Http.HTTP_GET, Http.HTTP_POST], detail=True, url_path="assignments")
    def assignments(self, request, pk=None):
        order = self.get_object()
        
        if request.method == 'GET':
            assignments = Assignment.objects.filter(order=order)
            serializer = AssignmentSerializer(assignments, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            created_assignments = []
            
            for assignment_data in request.data:
                assignment_data['order'] = order.id
                serializer = AssignmentSerializer(data=assignment_data)
                
                if serializer.is_valid():
                    assignment = serializer.save()
                    created_assignments.append(assignment)
                else:
                    return Response(
                        {
                            "detail": "Dữ liệu không hợp lệ",
                            "errors": serializer.errors
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            result_serializer = AssignmentSerializer(created_assignments, many=True)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)

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
