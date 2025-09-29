from base.views import BaseViewSet
from rest_framework import viewsets, permissions
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
from rest_framework import status

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
                if self.action in ['list', 'retrieve', 'assignments']:
                    return [permissions.IsAuthenticated(), IsEmployee()]
                return [permissions.IsAdminUser()]
            elif user.role in ['customer', 'guest']:
                if self.action in ['list', 'retrieve', 'create']:
                    return [permissions.IsAuthenticated(), IsCustomer()]
                return [permissions.IsAdminUser()]
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
            print("Received data:", request.data)  # Thêm log để debug
            
            for assignment_data in request.data:
                assignment_data['order'] = order.id
                serializer = AssignmentSerializer(data=assignment_data)
                print("Validating data:", assignment_data)  # Thêm log để debug
                
                if serializer.is_valid():
                    assignment = serializer.save()
                    created_assignments.append(assignment)
                else:
                    print("Validation errors:", serializer.errors)  # Thêm log để debug
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
