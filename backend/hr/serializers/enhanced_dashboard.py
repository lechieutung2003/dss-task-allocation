"""
Enhanced Dashboard Serializers
"""
from rest_framework import serializers


# ==================== MODULE 1: PRIORITY ORDERS ====================

class PriorityOrderEnhancedSerializer(serializers.Serializer):
    """Serializer cho Priority Orders Module"""
    order_id = serializers.CharField()
    code = serializers.CharField()
    price = serializers.FloatField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    status = serializers.CharField()
    time_factor = serializers.FloatField()
    price_factor = serializers.FloatField()
    priority_score = serializers.FloatField()
    hours_left = serializers.CharField() 
    time_bucket = serializers.CharField()
    customer_name = serializers.CharField()
    service_type = serializers.CharField()
    area_m2 = serializers.FloatField()


# ==================== MODULE 2: EMPLOYEE KPI ====================

class EmployeeKPIEnhancedSerializer(serializers.Serializer):
    """Serializer cho Employee KPI Module"""
    employee_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    total_worked_hours = serializers.FloatField()
    work_hour_score = serializers.FloatField()
    early_bonus = serializers.FloatField()
    kpi_score = serializers.FloatField()
    completed_orders = serializers.IntegerField()
    area = serializers.CharField()


class OrderDetailSerializer(serializers.Serializer):
    """Serializer cho chi tiết order trong KPI detail"""
    order_id = serializers.CharField()
    code = serializers.CharField()
    service_type = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    actual_end = serializers.DateTimeField(allow_null=True)
    worked_hours = serializers.FloatField()
    early_bonus = serializers.FloatField()
    cost = serializers.FloatField()


class EmployeeKPIDetailSerializer(serializers.Serializer):
    """Serializer cho popup chi tiết KPI nhân viên"""
    employee_id = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    area = serializers.CharField()
    total_worked_hours = serializers.FloatField()
    work_hour_score = serializers.FloatField()
    early_bonus_total = serializers.FloatField()
    kpi_score = serializers.FloatField()
    completed_orders_count = serializers.IntegerField()
    orders_detail = OrderDetailSerializer(many=True)


# ==================== MODULE 3: REVENUE - COST - PROFIT ====================

class RevenueCostProfitSerializer(serializers.Serializer):
    """Serializer cho Revenue/Cost/Profit Module"""
    date = serializers.CharField()
    revenue = serializers.FloatField()
    cost = serializers.FloatField()
    profit = serializers.FloatField()


# ==================== MAIN RESPONSE ====================

class EnhancedDashboardResponseSerializer(serializers.Serializer):
    """Main response serializer for enhanced dashboard"""
    priority_orders = PriorityOrderEnhancedSerializer(many=True)
    employee_kpi = EmployeeKPIEnhancedSerializer(many=True)
    revenue_cost_profit = RevenueCostProfitSerializer(many=True)
