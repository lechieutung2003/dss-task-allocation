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