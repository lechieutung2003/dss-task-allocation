"""
Dashboard Serializers - Serialize dữ liệu dashboard cho JSON response
"""
from rest_framework import serializers
from decimal import Decimal


class PriorityOrderSerializer(serializers.Serializer):
    """Serializer cho orders ưu tiên"""
    order_id = serializers.IntegerField()
    priority_score = serializers.FloatField()
    priority_level = serializers.CharField()
    time_score = serializers.FloatField()
    price_score = serializers.FloatField()
    preferred_start_time = serializers.DateTimeField()
    preferred_end_time = serializers.DateTimeField()
    cost_confirm = serializers.DecimalField(max_digits=10, decimal_places=2)
    service_type = serializers.CharField()
    service_type_id = serializers.IntegerField()
    status = serializers.CharField()
    customer_name = serializers.CharField()
    customer_id = serializers.IntegerField()
    area_m2 = serializers.DecimalField(max_digits=10, decimal_places=2)
    estimated_hours = serializers.DecimalField(max_digits=5, decimal_places=2)
    note = serializers.CharField(allow_blank=True)


class EmployeeKPISerializer(serializers.Serializer):
    """Serializer cho KPI nhân viên"""
    employee_id = serializers.IntegerField()
    name = serializers.CharField()
    completed_orders = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    avg_duration = serializers.FloatField()
    completion_rate = serializers.FloatField()
    kpi_score = serializers.FloatField()
    total_hours_worked = serializers.FloatField()
    area = serializers.CharField()


class DailySummarySerializer(serializers.Serializer):
    """Serializer cho tổng hợp theo ngày"""
    date = serializers.CharField()  # ISO format date string
    revenue = serializers.FloatField()
    cost = serializers.FloatField()
    profit = serializers.FloatField()
    complete_count = serializers.IntegerField()
    reject_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()
    total_orders = serializers.IntegerField()


class DashboardOverviewSerializer(serializers.Serializer):
    """Serializer cho tổng quan dashboard"""
    total_orders = serializers.IntegerField()
    active_orders = serializers.IntegerField()
    completed_orders = serializers.IntegerField()
    rejected_orders = serializers.IntegerField()
    success_rate = serializers.FloatField()
    total_revenue = serializers.FloatField()
    total_cost = serializers.FloatField()
    total_profit = serializers.FloatField()
    profit_margin = serializers.FloatField()
    active_employees = serializers.IntegerField()
    avg_completion_time = serializers.FloatField()


class DashboardResponseSerializer(serializers.Serializer):
    """
    Main dashboard response serializer
    Tổng hợp tất cả data cần thiết cho frontend dashboard
    """
    overview = DashboardOverviewSerializer()
    priority_orders = PriorityOrderSerializer(many=True)
    employee_kpi = EmployeeKPISerializer(many=True)
    daily_summary = DailySummarySerializer(many=True)
