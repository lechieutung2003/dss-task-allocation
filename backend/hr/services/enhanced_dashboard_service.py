"""
Enhanced Dashboard Service - Complete system with 3 modules
"""
from django.db.models import Q, Count, Avg, Sum, F, DecimalField, ExpressionWrapper, FloatField
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any
from oauth.models.user import User
from hr.models.order import Order, Assignment
from businesses.models.employee import Employee


class EnhancedDashboardService:
    """Complete Dashboard Service with 3 modules"""
    
    # ==================== MODULE 1: PRIORITY ORDERS ====================
    
    @staticmethod
    def clean_orders_for_priority():
        """Clean data: loại bỏ records lỗi, null, thời gian không hợp lệ"""
        return Order.objects.filter(
            preferred_start_time__isnull=False,
            preferred_end_time__isnull=False,
            cost_confirm__isnull=False,
            cost_confirm__gt=0,
            preferred_start_time__lt=F('preferred_end_time'),  # Validate time logic
            status__in=['pending', 'in_progress']  # Chỉ lấy đơn chưa hoàn thành
        )
    
    @staticmethod
    def calculate_priority_factors(order: Order) -> Dict[str, Any]:
        """
        Tính Time Factor và Price Factor cho đơn hàng
        """
        now = timezone.now()
        time_diff = (order.preferred_start_time - now - timedelta(hours=7)).total_seconds()
        hours_left = time_diff / 3600

        # Chuyển đổi sang giờ-phút
        if hours_left >= 0:
            hours_int = int(hours_left)
            minutes_int = int(round((hours_left - hours_int) * 60))
            hours_left_str = f"{hours_int}h{minutes_int}p"
        else:
            hours_left_str = "Đã quá hạn"

        # Time Factor
        if 1 < hours_left <= 2:
            time_factor = 0.7
        elif 2 < hours_left <= 3:
            time_factor = 0.6
        elif 3 < hours_left <= 4:
            time_factor = 0.5
        elif 4 < hours_left <= 5:
            time_factor = 0.4
        elif 5 < hours_left <= 8:
            time_factor = 0.3
        elif 8 < hours_left <= 12:
            time_factor = 0.2
        elif 12 < hours_left <= 24:
            time_factor = 0.1
        else:
            time_factor = 0

        # Price Factor
        ref_price = 2000
        price = float(order.cost_confirm or 0)
        price_factor = 0.3 * min(price / ref_price, 1)

        # Priority Score
        priority_score = round(time_factor + price_factor, 3)

        return {
            'time_factor': round(time_factor, 3),
            'price_factor': round(price_factor, 3),
            'priority_score': priority_score,                      
            'hours_left': hours_left_str,  # Trả về dạng "xh ym"
            'time_bucket': EnhancedDashboardService._get_time_bucket(hours_left)
        }
    
    @staticmethod
    def _get_time_bucket(hours_left: float) -> str:
        """Xác định bucket thời gian để nhóm các đơn"""
        if 1 < hours_left <= 2:
            return '1-2h'
        elif 2 < hours_left <= 3:
            return '2-3h'
        elif 3 < hours_left <= 4:
            return '3-4h'
        elif 4 < hours_left <= 5:
            return '4-5h'
        elif 5 < hours_left <= 8:
            return '5-8h'
        elif 8 < hours_left <= 12:
            return '8-12h'
        elif 12 < hours_left <= 24:
            return '12-24h'
        else:
            return '24h+'
    
    @staticmethod
    def get_priority_orders_top10() -> List[Dict[str, Any]]:
        cleaned_orders = EnhancedDashboardService.clean_orders_for_priority()
        result = []
        for order in cleaned_orders:
            try:
                factors = EnhancedDashboardService.calculate_priority_factors(order)
                result.append({
                    'order_id': str(order.id),
                    'code': f'ORD-{str(order.id)[:8]}',
                    'price': float(order.cost_confirm or 0),
                    'start_time': order.preferred_start_time.isoformat() if order.preferred_start_time else '',
                    'end_time': order.preferred_end_time.isoformat() if order.preferred_end_time else '',
                    'status': order.status or '',
                    'time_factor': factors.get('time_factor', 0),
                    'price_factor': factors.get('price_factor', 0),
                    'priority_score': factors.get('priority_score', 0),
                    'hours_left': factors.get('hours_left', 0),
                    'time_bucket': factors.get('time_bucket', ''),
                    'customer_name': order.customer.name if order.customer else '',
                    'service_type': order.service_type.name if order.service_type else '',
                    'area_m2': float(order.area_m2 or 0),
                })
            except Exception as e:
                print(f"❌ Error in get_priority_orders_top10 for order {order.id}: {e}")
                import traceback
                traceback.print_exc()
        
        # Sort theo quy tắc:
        # 1. Time bucket (thứ tự ưu tiên: 1-2h, 2-3h, 3-4h, ...)
        # 2. Trong cùng bucket, sort theo priority_score giảm dần
        bucket_order = ['1-2h', '2-3h', '3-4h', '4-5h', '5-8h', '8-12h', '12-24h', '24h+']
        
        result.sort(
            key=lambda x: (
                bucket_order.index(x['time_bucket']) if x['time_bucket'] in bucket_order else 999,
                -x['priority_score']
            )
        )
        
        return result[:10]
    
    # ==================== MODULE 2: EMPLOYEE KPI ====================

    # @staticmethod
    # def calculate_employee_kpi_enhanced() -> List[Dict[str, Any]]:
    #     """
    #     Tính KPI nhân viên dựa trên dữ liệu tổng hợp ở bảng Employee.
    #     """
    #     try:
    #         employees = Employee.objects.filter(user__is_staff=True, user__is_superuser=False)
    #     except Exception as e:
    #         print(f"❌ Error filtering employees: {e}")
    #         return []

    #     result = []
    #     for emp in employees:
    #         total_worked_hours = float(emp.total_hours_worked or 0)
    #         order_count = int(emp.completed_orders_count or 0)
    #         early_bonus = 0  # Nếu muốn tính, cần lấy từ Order hoặc lưu riêng

    #         daily_standard = 8.0
    #         work_hour_score = min(total_worked_hours / daily_standard, 1) if daily_standard > 0 else 0
    #         kpi_score = round(work_hour_score + early_bonus, 3)

    #         try:
    #             result.append({
    #                 'employee_id': emp.id,
    #                 'name': f"{emp.first_name} {emp.last_name}".strip() or 'Unknown',
    #                 'email': emp.work_mail or emp.personal_mail or 'N/A',
    #                 'total_worked_hours': round(total_worked_hours, 2),
    #                 'work_hour_score': round(work_hour_score, 3),
    #                 'early_bonus': round(early_bonus, 3),
    #                 'kpi_score': kpi_score,
    #                 'completed_orders': order_count,
    #                 'area': getattr(emp, 'area', 'N/A') or 'N/A',
    #             })
    #         except Exception as e:
    #             print(f"❌ Error appending employee {emp.id} to result: {e}")
    #             continue

    #     result.sort(key=lambda x: x['kpi_score'], reverse=True)
    #     return result
    
    
    @staticmethod
    def calculate_employee_kpi_enhanced() -> List[Dict[str, Any]]:
        """
        Tính KPI nhân viên: KPI = tổng số giờ làm + số đơn hoàn thành.
        """
        try:
            employees = Employee.objects.filter(user__is_staff=True, user__is_superuser=False)
        except Exception as e:
            print(f"❌ Error filtering employees: {e}")
            return []

        result = []
        for emp in employees:
            try:
                total_worked_hours = float(emp.total_hours_worked or 0)
                order_count = int(emp.completed_orders_count or 0)
                kpi_score = total_worked_hours + order_count

                result.append({
                    'employee_id': str(emp.id),  # ép kiểu về string để an toàn
                    'name': f"{getattr(emp, 'first_name', '')} {getattr(emp, 'last_name', '')}".strip() or 'Unknown',
                    'email': getattr(emp, 'work_mail', '') or getattr(emp, 'personal_mail', '') or 'N/A',
                    'total_worked_hours': round(total_worked_hours, 2),
                    'work_hour_score': round(total_worked_hours, 2),  # Same as total_worked_hours
                    'early_bonus': 0.0,  # No bonus in simplified version
                    'completed_orders': order_count,
                    'area': 'N/A',  # Add area field if available
                    'kpi_score': round(kpi_score, 2),
                })
            except Exception as e:
                print(f"❌ Error appending employee {getattr(emp, 'id', None)} to result: {e}")
                import traceback
                traceback.print_exc()
                continue

        result.sort(key=lambda x: x['kpi_score'], reverse=True)
        return result
    
    @staticmethod
    def get_employee_kpi_detail(employee_id: int) -> Dict[str, Any]:
        """
        Chi tiết KPI của 1 nhân viên (cho popup)
        Lấy từ bảng Employee (total_hours_worked, completed_orders_count) 
        và từ bảng trung gian Order.employees để hiển thị chi tiết các đơn
        """
        try:
            emp = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return None
        
        # Lấy tổng số giờ và số đơn từ bảng Employee
        total_worked_hours = float(emp.total_hours_worked or 0)
        completed_orders_count = int(emp.completed_orders_count or 0)
        
        # Lấy danh sách các đơn đã hoàn thành từ bảng trung gian Order.employees
        completed_orders = emp.orders.filter(status='completed').order_by('-updated_at')
        
        orders_detail = []
        early_bonus_total = 0
        
        for order in completed_orders:
            # Tính early bonus per order
            early_bonus_order = 0
            if order.updated_at and order.preferred_end_time:
                actual_end = order.updated_at
                expected_end = order.preferred_end_time
                
                if timezone.is_naive(actual_end):
                    actual_end = timezone.make_aware(actual_end)
                if timezone.is_naive(expected_end):
                    expected_end = timezone.make_aware(expected_end)
                
                if actual_end < expected_end:
                    if order.preferred_start_time:
                        expected_duration = (expected_end - order.preferred_start_time).total_seconds() / 3600
                        time_saved = (expected_end - actual_end).total_seconds() / 3600
                        
                        if expected_duration > 0:
                            early_bonus_order = time_saved / expected_duration
                            early_bonus_total += early_bonus_order
            
            # Tính worked_hours: min của estimated_hours và requested_hours
            estimated_h = float(order.estimated_hours or 0)
            requested_h = float(order.requested_hours or 0)
            
            if estimated_h > 0 and requested_h > 0:
                worked_hours = min(estimated_h, requested_h)
            elif estimated_h > 0:
                worked_hours = estimated_h
            elif requested_h > 0:
                worked_hours = requested_h
            else:
                worked_hours = 0
            
            orders_detail.append({
                'order_id': str(order.id),
                'code': f'ORD-{str(order.id)[:8]}',
                'service_type': order.service_type.name if order.service_type else 'N/A',
                'start_time': order.preferred_start_time,
                'end_time': order.preferred_end_time,
                'actual_end': order.updated_at,
                'worked_hours': round(worked_hours, 2),
                'early_bonus': round(early_bonus_order, 3),
                'cost': float(order.cost_confirm or 0),
            })
        
        # Tính KPI score: total_worked_hours + completed_orders_count
        kpi_score = total_worked_hours + completed_orders_count
        
        return {
            'employee_id': str(emp.id),
            'name': f"{emp.first_name} {emp.last_name}".strip() or 'Unknown',
            'email': emp.work_mail or emp.personal_mail or 'N/A',
            'area': getattr(emp, 'area', 'N/A') or 'N/A',
            'total_worked_hours': round(total_worked_hours, 2),
            'work_hour_score': round(total_worked_hours, 2),
            'early_bonus_total': round(early_bonus_total, 3),
            'kpi_score': round(kpi_score, 2),
            'completed_orders_count': completed_orders_count,
            'orders_detail': orders_detail
        }
    
    # ==================== MODULE 3: REVENUE - COST - PROFIT ====================
    
    @staticmethod
    def clean_orders_for_revenue():
        """Clean data: loại records lỗi, null, thời gian âm"""
        return Order.objects.filter(
            preferred_start_time__isnull=False,
            preferred_end_time__isnull=False,
            cost_confirm__isnull=False,
            cost_confirm__gt=0,
            preferred_start_time__lt=F('preferred_end_time'),
            status='completed'
        )
    
    @staticmethod
    def calculate_revenue_cost_profit(start_date=None, end_date=None, period='day') -> List[Dict[str, Any]]:
        """
        Tính Revenue - Cost - Profit theo ngày/tuần/tháng
        
        Revenue: cost_confirm của orders completed
        Cost: 20 * (giờ kết thúc - giờ bắt đầu) * số nhân viên làm đơn
        Profit: Revenue - Cost
        
        Args:
            start_date: datetime
            end_date: datetime
            period: 'day' | 'week' | 'month'
        """
        if end_date is None:
            end_date = timezone.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Clean orders
        orders = EnhancedDashboardService.clean_orders_for_revenue().filter(
            updated_at__gte=start_date,
            updated_at__lte=end_date
        )
        
        # Group by period
        if period == 'week':
            orders_grouped = orders.annotate(period_date=TruncWeek('updated_at'))
        elif period == 'month':
            orders_grouped = orders.annotate(period_date=TruncMonth('updated_at'))
        else:  # day
            orders_grouped = orders.annotate(period_date=TruncDate('updated_at'))
        
        # Aggregate revenue
        revenue_data = orders_grouped.values('period_date').annotate(
            revenue=Sum('cost_confirm', output_field=DecimalField())
        ).order_by('period_date')
        
        # Tính cost cho từng order
        result = {}
        for order in orders:
            # Period key
            if period == 'week':
                period_key = order.updated_at.date() - timedelta(days=order.updated_at.weekday())
            elif period == 'month':
                period_key = order.updated_at.date().replace(day=1)
            else:
                period_key = order.updated_at.date()
            
            if period_key not in result:
                result[period_key] = {
                    'date': period_key.isoformat(),
                    'revenue': 0,
                    'cost': 0,
                    'profit': 0
                }
            
            # Revenue
            result[period_key]['revenue'] += float(order.cost_confirm or 0)
            
            # Cost calculation: 20 * (end - start in hours) * số nhân viên
            duration_hours = (order.preferred_end_time - order.preferred_start_time).total_seconds() / 3600
            employee_count = Assignment.objects.filter(order=order).count()
            
            if employee_count == 0:
                employee_count = 1  # Default nếu không có assignment
            
            cost = 20 * duration_hours * employee_count
            result[period_key]['cost'] += cost
        
        # Calculate profit
        final_result = []
        for date_key in sorted(result.keys()):
            data = result[date_key]
            data['profit'] = data['revenue'] - data['cost']
            
            # Round values
            data['revenue'] = round(data['revenue'], 2)
            data['cost'] = round(data['cost'], 2)
            data['profit'] = round(data['profit'], 2)
            
            final_result.append(data)
        
        return final_result
