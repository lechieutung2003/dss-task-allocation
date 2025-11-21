"""
Dashboard Service - Xử lý data cleaning, tính toán KPI và tổng hợp dữ liệu cho dashboard
"""
from django.db.models import Q, Count, Avg, Sum, F, DecimalField, ExpressionWrapper
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any

from hr.models.order import Order, Assignment
from businesses.models.employee import Employee


class DashboardService:
    """Service xử lý tất cả logic cho dashboard admin"""
    
    @staticmethod
    def clean_orders_data(queryset=None):
        """
        Data Cleaning: Lọc và chuẩn hóa dữ liệu orders
        - Loại bỏ đơn thiếu preferred_start_time hoặc cost_confirm
        - Chuẩn hóa thời gian về datetime
        - Chuẩn hóa cost_confirm về VND
        - Loại bỏ trùng lặp
        """
        if queryset is None:
            queryset = Order.objects.all()
        
        # Loại bỏ các đơn thiếu thông tin quan trọng
        cleaned_orders = queryset.filter(
            preferred_start_time__isnull=False,
            cost_confirm__isnull=False,
            cost_confirm__gt=0  # Cost phải > 0
        ).distinct()
        
        return cleaned_orders.select_related(
            'customer', 
            'service_type'
        ).order_by('-created_at')
    
    @staticmethod
    # def calculate_priority_score(order: Order) -> Dict[str, Any]:
    #     """
    #     Tính priority score cho từng order:
    #     - Thời gian gần (weight 0.6) → scale 0–0.6
    #     - Giá thành cao (cost_confirm) (weight 0.4) → scale 0–0.4
    #     - Total priority = time_score + price_score
        
    #     Returns:
    #         {
    #             'time_score': float,
    #             'price_score': float,
    #             'priority_score': float,
    #             'priority_level': str  # 'high', 'medium', 'low'
    #         }
    #     """
    #     now = timezone.now()
        
    #     # 1. Tính time_score (0-0.6)
    #     # Đơn càng gần deadline càng có điểm cao
    #     time_diff = (order.preferred_start_time - now).total_seconds()
    #     hours_left = time_diff / 3600
        
    #     if hours_left < 0:
    #         # Quá hạn → priority cao nhất
    #         time_score = 0.6
    #     elif hours_left <= 24:
    #         # < 24h → 0.5-0.6
    #         time_score = 0.5 + (0.1 * (1 - hours_left / 24))
    #     elif hours_left <= 72:
    #         # < 72h → 0.3-0.5
    #         time_score = 0.3 + (0.2 * (1 - (hours_left - 24) / 48))
    #     elif hours_left <= 168:
    #         # < 1 tuần → 0.1-0.3
    #         time_score = 0.1 + (0.2 * (1 - (hours_left - 72) / 96))
    #     else:
    #         # > 1 tuần → 0-0.1
    #         time_score = max(0, 0.1 * (1 - (hours_left - 168) / 336))
        
    #     # 2. Tính price_score (0-0.4)
    #     # Giá cao → score cao
    #     cost = float(order.cost_confirm or 0)
        
    #     # Normalize dựa trên range của cost trong DB
    #     # Giả sử cost từ 100k - 10M VND
    #     min_cost = 100000
    #     max_cost = 10000000
        
    #     if cost >= max_cost:
    #         price_score = 0.4
    #     elif cost <= min_cost:
    #         price_score = 0.0
    #     else:
    #         # Linear scaling
    #         price_score = 0.4 * ((cost - min_cost) / (max_cost - min_cost))
        
    #     # 3. Tính tổng priority_score
    #     priority_score = round(time_score + price_score, 2)
        
    #     # 4. Phân loại level
    #     if priority_score >= 0.7:
    #         priority_level = 'high'
    #     elif priority_score >= 0.4:
    #         priority_level = 'medium'
    #     else:
    #         priority_level = 'low'
        
    #     return {
    #         'time_score': round(time_score, 2),
    #         'price_score': round(price_score, 2),
    #         'priority_score': priority_score,
    #         'priority_level': priority_level
    #     }
    
    @staticmethod
    def calculate_priority_score(order: Order) -> Dict[str, Any]:
        """
        Tính priority score cho từng order:
        - Thời gian bắt đầu sát giờ hiện tại (70%)
        - Giá thành cao hơn (30%)
        """
        now = timezone.now()
        time_diff = (order.preferred_start_time - now).total_seconds()
        hours_left = time_diff / 3600

        # Thời gian (70%)
        if 1 < hours_left <= 2:
            time_score = 0.7
        elif 2 < hours_left <= 3:
            time_score = 0.6
        elif 3 < hours_left <= 4:
            time_score = 0.5
        elif 4 < hours_left <= 5:
            time_score = 0.4
        elif 5 < hours_left <= 8:
            time_score = 0.3
        elif 8 < hours_left <= 12:
            time_score = 0.2
        elif 12 < hours_left <= 24:
            time_score = 0.1
        else:
            time_score = 0

        # Giá thành (30%)
        ref_price = 2000000
        cost = float(order.cost_confirm or 0)
        price_score = 0.3 * min(cost / ref_price, 1)

        # Tổng điểm
        priority_score = round(time_score + price_score, 3)

        # Phân loại level
        if priority_score >= 0.7:
            priority_level = 'high'
        elif priority_score >= 0.4:
            priority_level = 'medium'
        else:
            priority_level = 'low'

        return {
            'time_score': round(time_score, 3),
            'price_score': round(price_score, 3),
            'priority_score': priority_score,
            'priority_level': priority_level
        }
    @staticmethod
    @staticmethod
    def get_priority_orders(limit=20) -> List[Dict[str, Any]]:
        """
        Lấy danh sách orders ưu tiên, đã clean và tính priority score
        - Ưu tiên theo giờ bắt đầu gần nhất (giảm dần)
        - Nếu cùng giờ thì ưu tiên giá cao hơn (giảm dần)
        """
        cleaned_orders = DashboardService.clean_orders_data()
        pending_orders = cleaned_orders.filter(
            status__in=['pending']
        )

        result = []
        for order in pending_orders:
            priority_data = DashboardService.calculate_priority_score(order)
            result.append({
                'order_id': order.id,
                'priority_score': priority_data['priority_score'],
                'priority_level': priority_data['priority_level'],
                'time_score': priority_data['time_score'],
                'price_score': priority_data['price_score'],
                'preferred_start_time': order.preferred_start_time,
                'preferred_end_time': order.preferred_end_time,
                'cost_confirm': order.cost_confirm,
                'service_type': order.service_type.name,
                'service_type_id': order.service_type.id,
                'status': order.status,
                'customer_name': order.customer.name,
                'customer_id': order.customer.id,
                'area_m2': order.area_m2,
                'estimated_hours': order.estimated_hours,
                'note': order.note or '',
            })

        # Sắp xếp: 1. Giờ bắt đầu gần nhất (tăng dần), 2. Giá cao hơn (giảm dần)
        result.sort(
            key=lambda x: (
                abs((x['preferred_start_time'] - timezone.now()).total_seconds()),
                -float(x['cost_confirm'] or 0)
            )
        )

        return result[:limit]
    
    @staticmethod
    def calculate_employee_kpi() -> List[Dict[str, Any]]:
        """
        Tính KPI cho từng nhân viên:
        - Số đơn đã làm
        - Thời lượng trung bình (estimated_hours)
        - % công việc hoàn thành
        
        Returns:
            List of dicts:
            {
                'employee_id': int,
                'name': str,
                'completed_orders': int,
                'avg_duration': Decimal,
                'completion_rate': float,
                'kpi_score': float,  # 0-100
                'total_hours_worked': Decimal,
            }
        """
        # Lấy tất cả assignments và tính KPI
        employees = Employee.objects.filter(
            status=1  # Active employees only
        ).annotate(
            total_assignments=Count('assignment'),
            completed_assignments=Count(
                'assignment',
                filter=Q(assignment__status='completed')
            ),
            avg_work_hours=Avg('assignment__work_hours'),
            total_work_hours=Sum('assignment__work_hours')
        )
        
        result = []
        for emp in employees:
            total = emp.total_assignments or 0
            completed = emp.completed_assignments or 0
            
            # Completion rate
            completion_rate = (completed / total * 100) if total > 0 else 0.0
            
            # KPI Score (weighted average)
            # - 50% từ completion_rate
            # - 30% từ số lượng đơn hoàn thành (normalize)
            # - 20% từ total hours worked (normalize)
            
            # Normalize completed orders (giả sử max 100 đơn/tháng)
            completed_normalized = min(completed / 100.0 * 100, 100)
            
            # Normalize hours (giả sử max 200h/tháng)
            hours = float(emp.total_work_hours or 0)
            hours_normalized = min(hours / 200.0 * 100, 100)
            
            kpi_score = (
                0.5 * completion_rate +
                0.3 * completed_normalized +
                0.2 * hours_normalized
            )
            
            result.append({
                'employee_id': emp.id,
                'name': f"{emp.first_name} {emp.last_name}".strip(),
                'completed_orders': completed,
                'total_orders': total,
                'avg_duration': round(float(emp.avg_work_hours or 0), 2),
                'completion_rate': round(completion_rate, 2),
                'kpi_score': round(kpi_score, 2),
                'total_hours_worked': float(emp.total_work_hours or 0),
                'area': emp.area or 'N/A',
            })
        
        # Sort by KPI score descending
        result.sort(key=lambda x: x['kpi_score'], reverse=True)
        
        return result
    
    @staticmethod
    def calculate_daily_summary(start_date=None, end_date=None) -> List[Dict[str, Any]]:
        """
        Tổng hợp kinh doanh theo ngày:
        - Revenue (doanh thu từ cost_confirm của orders completed)
        - Cost (chi phí từ assignments)
        - Profit = Revenue - Cost
        - Số đơn success/fail theo ngày
        
        Args:
            start_date: datetime, mặc định 30 ngày trước
            end_date: datetime, mặc định hôm nay
            
        Returns:
            List of dicts:
            {
                'date': date,
                'revenue': Decimal,
                'cost': Decimal,
                'profit': Decimal,
                'complete_count': int,
                'reject_count': int,
                'pending_count': int,
                'total_orders': int,
            }
        """
        if end_date is None:
            end_date = timezone.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Clean data - sử dụng preferred_start_time thay vì created_at
        orders = DashboardService.clean_orders_data().filter(
            preferred_start_time__date__gte=start_date.date(),
            preferred_start_time__date__lte=end_date.date()
        )
        
        # Group by date of preferred_start_time
        daily_data = orders.annotate(
            date=TruncDate('preferred_start_time')
        ).values('date').annotate(
            total_orders=Count('id'),
            complete_count=Count('id', filter=Q(status='completed')),
            reject_count=Count('id', filter=Q(status='rejected')),
            pending_count=Count('id', filter=Q(status__in=['pending', 'confirmed', 'in_progress'])),
            # Revenue từ orders completed
            revenue=Sum(
                'cost_confirm',
                filter=Q(status='completed'),
                output_field=DecimalField()
            )
        ).order_by('date')
        
        # Lấy cost từ assignments theo date
        assignments = Assignment.objects.filter(
            assigned_time__date__gte=start_date.date(),
            assigned_time__date__lte=end_date.date()
        ).annotate(
            date=TruncDate('assigned_time')
        ).values('date').annotate(
            total_cost=Sum('cost', output_field=DecimalField())
        )
        
        # Map cost theo date
        cost_map = {item['date']: item['total_cost'] for item in assignments}
        
        # Combine data
        result = []
        for item in daily_data:
            date = item['date']
            revenue = item['revenue'] or Decimal('0')
            cost = cost_map.get(date, Decimal('0'))
            profit = revenue - cost
            
            result.append({
                'date': date.isoformat(),
                'revenue': float(revenue),
                'cost': float(cost),
                'profit': float(profit),
                'complete_count': item['complete_count'],
                'reject_count': item['reject_count'],
                'pending_count': item['pending_count'],
                'total_orders': item['total_orders'],
            })
        
        return result
    
    @staticmethod
    def get_dashboard_overview() -> Dict[str, Any]:
        """
        Lấy tổng quan dashboard:
        - Tổng số orders (total, active, completed, failed)
        - Tổng doanh thu, chi phí, lợi nhuận
        - Số nhân viên active
        - Average completion time
        """
        cleaned_orders = DashboardService.clean_orders_data()
        
        total_orders = cleaned_orders.count()
        completed_orders = cleaned_orders.filter(status='completed').count()
        active_orders = cleaned_orders.filter(
            status__in=['pending', 'confirmed', 'in_progress']
        ).count()
        rejected_orders = cleaned_orders.filter(status='rejected').count()
        
        # Revenue & Cost
        revenue = cleaned_orders.filter(status='completed').aggregate(
            total=Sum('cost_confirm')
        )['total'] or Decimal('0')
        
        cost = Assignment.objects.aggregate(
            total=Sum('cost')
        )['total'] or Decimal('0')
        
        profit = revenue - cost
        
        # Employee stats
        active_employees = Employee.objects.filter(status=1).count()
        
        # Average completion time
        avg_completion = cleaned_orders.filter(status='completed').aggregate(
            avg=Avg('estimated_hours')
        )['avg'] or Decimal('0')
        
        return {
            'total_orders': total_orders,
            'active_orders': active_orders,
            'completed_orders': completed_orders,
            'rejected_orders': rejected_orders,
            'success_rate': round((completed_orders / total_orders * 100) if total_orders > 0 else 0, 2),
            'total_revenue': float(revenue),
            'total_cost': float(cost),
            'total_profit': float(profit),
            'profit_margin': round((float(profit) / float(revenue) * 100) if revenue > 0 else 0, 2),
            'active_employees': active_employees,
            'avg_completion_time': round(float(avg_completion), 2),
        }
