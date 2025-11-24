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
    
    # @staticmethod
    # def clean_orders_for_revenue():
    #     """Clean data: loại records lỗi, null, thời gian âm"""
    #     return Order.objects.filter(
    #         preferred_start_time__isnull=False,
    #         preferred_end_time__isnull=False,
    #         cost_confirm__isnull=False,
    #         cost_confirm__gt=0,
    #         preferred_start_time__lt=F('preferred_end_time'),
    #         status='completed'
    #     )
    
    # @staticmethod
    # def calculate_revenue_cost_profit(start_date=None, end_date=None, period='day') -> List[Dict[str, Any]]:
    #     """
    #     Tính Revenue - Cost - Profit theo ngày/tuần/tháng
        
    #     Revenue: cost_confirm của orders completed
    #     Cost: 20 * (giờ kết thúc - giờ bắt đầu) * số nhân viên làm đơn
    #     Profit: Revenue - Cost
        
    #     Args:
    #         start_date: datetime
    #         end_date: datetime
    #         period: 'day' | 'week' | 'month'
    #     """
    #     if end_date is None:
    #         end_date = timezone.now()
    #     if start_date is None:
    #         start_date = end_date - timedelta(days=30)
        
    #     # Clean orders
    #     orders = EnhancedDashboardService.clean_orders_for_revenue().filter(
    #         updated_at__gte=start_date,
    #         updated_at__lte=end_date
    #     )
        
    #     # Group by period
    #     if period == 'week':
    #         orders_grouped = orders.annotate(period_date=TruncWeek('updated_at'))
    #     elif period == 'month':
    #         orders_grouped = orders.annotate(period_date=TruncMonth('updated_at'))
    #     else:  # day
    #         orders_grouped = orders.annotate(period_date=TruncDate('updated_at'))
        
    #     # Aggregate revenue
    #     revenue_data = orders_grouped.values('period_date').annotate(
    #         revenue=Sum('cost_confirm', output_field=DecimalField())
    #     ).order_by('period_date')
        
    #     # Tính cost cho từng order
    #     result = {}
    #     for order in orders:
    #         # Period key
    #         if period == 'week':
    #             period_key = order.updated_at.date() - timedelta(days=order.updated_at.weekday())
    #         elif period == 'month':
    #             period_key = order.updated_at.date().replace(day=1)
    #         else:
    #             period_key = order.updated_at.date()
            
    #         if period_key not in result:
    #             result[period_key] = {
    #                 'date': period_key.isoformat(),
    #                 'revenue': 0,
    #                 'cost': 0,
    #                 'profit': 0
    #             }
            
    #         # Revenue
    #         result[period_key]['revenue'] += float(order.cost_confirm or 0)
            
    #         # Cost calculation: 20 * (end - start in hours) * số nhân viên
    #         duration_hours = (order.preferred_end_time - order.preferred_start_time).total_seconds() / 3600
    #         employee_count = Assignment.objects.filter(order=order).count()
            
    #         if employee_count == 0:
    #             employee_count = 1  # Default nếu không có assignment
            
    #         cost = 20 * duration_hours * employee_count
    #         result[period_key]['cost'] += cost
        
    #     # Calculate profit
    #     final_result = []
    #     for date_key in sorted(result.keys()):
    #         data = result[date_key]
    #         data['profit'] = data['revenue'] - data['cost']
            
    #         # Round values
    #         data['revenue'] = round(data['revenue'], 2)
    #         data['cost'] = round(data['cost'], 2)
    #         data['profit'] = round(data['profit'], 2)
            
    #         final_result.append(data)
        
    #     return final_result
    
    
    
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
    def calculate_revenue_cost_profit(start_date=None, end_date=None, period='day', date_field: str = 'updated_at') -> List[Dict[str, Any]]:
        """
        Tính Revenue - Cost - Profit theo period:
        period must be one of: 'day', 'week', 'month', 'year'
        This wrapper also accepts ISO datetime strings for start_date/end_date.
        
        Args:
            start_date: datetime or str (ISO format)
            end_date: datetime or str (ISO format)
            period: 'day' | 'week' | 'month' | 'year'
            date_field: field name to use for filtering/labeling (e.g. 'updated_at', 'preferred_start_time', ...)
        """
        import calendar
        import traceback
        from decimal import Decimal, ROUND_HALF_UP

        try:
            # validate period
            allowed = {'day', 'week', 'month', 'year'}
            if period not in allowed:
                raise ValueError(f"Invalid period '{period}'. allowed: {allowed}")

            # parse start_date/end_date if they are ISO strings
            def _parse_dt(dt):
                if dt is None:
                    return None
                if isinstance(dt, str):
                    try:
                        return timezone.make_aware(datetime.fromisoformat(dt))
                    except Exception:
                        # fallback to parsing date only
                        return timezone.make_aware(datetime.fromisoformat(dt + 'T00:00:00'))
                return dt

            if end_date is None:
                end_date = timezone.now()
            end_date = _parse_dt(end_date) or end_date

            if start_date is None:
                start_date = end_date - timedelta(days=30)
            start_date = _parse_dt(start_date) or start_date

            # Ensure aware datetimes
            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date)
            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date)

            # Base queryset: completed orders in range using date_field
            filter_kwargs = {
                f"{date_field}__gte": start_date,
                f"{date_field}__lte": end_date
            }
            orders_qs = EnhancedDashboardService.clean_orders_for_revenue().filter(
                **filter_kwargs
            ).select_related('service_type', 'customer').prefetch_related('employees')

            # Debug: số orders trong range
            try:
                print(f"🔍 orders_qs count for range {start_date} - {end_date} (by {date_field}): {orders_qs.count()}")
            except Exception:
                print("🔍 cannot count orders_qs (debug)")

            # Prepare buckets structure (same logic as before)...
            buckets = []
            if period == 'week':
                # Use start_date directly as Monday (frontend already calculated correct week range)
                week_start = start_date.date()
                for i in range(7):
                    d = week_start + timedelta(days=i)
                    start_dt = datetime.combine(d, datetime.min.time()).replace(tzinfo=start_date.tzinfo)
                    end_dt = datetime.combine(d, datetime.max.time()).replace(tzinfo=start_date.tzinfo)
                    key = d.isoformat()
                    label = d.strftime('%a %d/%m')
                    buckets.append((key, label, start_dt, end_dt))
                    # Debug: print bucket range
                    if i == 1:  # only print second bucket to avoid spam
                        print(f"🪣 Sample bucket: {key} | start={start_dt} | end={end_dt}")
            elif period == 'month':
                # Use the middle of the range to determine which month to show
                mid_date = start_date + (end_date - start_date) / 2
                year = mid_date.year
                month = mid_date.month
                last_day = calendar.monthrange(year, month)[1]
                ranges = [(1,7), (8,14), (15,21), (22,last_day)]
                for idx, (sday, eday) in enumerate(ranges, start=1):
                    start_dt = datetime(year, month, sday, 0, 0, 0).replace(tzinfo=start_date.tzinfo)
                    end_dt = datetime(year, month, eday, 23, 59, 59, 999999).replace(tzinfo=start_date.tzinfo)
                    key = f"{year}-{month:02d}-w{idx}"
                    label = f"Tuần {idx} ({sday}-{eday})"
                    buckets.append((key, label, start_dt, end_dt))
            elif period == 'year':
                # Use the middle of the range to determine which year to show
                mid_date = start_date + (end_date - start_date) / 2
                year = mid_date.year
                for m in range(1, 13):
                    start_dt = datetime(year, m, 1, 0, 0, 0).replace(tzinfo=start_date.tzinfo)
                    last_day = calendar.monthrange(year, m)[1]
                    end_dt = datetime(year, m, last_day, 23, 59, 59, 999999).replace(tzinfo=start_date.tzinfo)
                    key = f"{year}-{m:02d}"
                    label = start_dt.strftime('%b %Y')
                    buckets.append((key, label, start_dt, end_dt))
            else:
                cur = start_date.date()
                end_date_only = end_date.date()
                while cur <= end_date_only:
                    start_dt = datetime.combine(cur, datetime.min.time()).replace(tzinfo=start_date.tzinfo)
                    end_dt = datetime.combine(cur, datetime.max.time()).replace(tzinfo=start_date.tzinfo)
                    key = cur.isoformat()
                    label = cur.strftime('%d/%m/%Y')
                    buckets.append((key, label, start_dt, end_dt))
                    cur = cur + timedelta(days=1)

            # Initialize result map (include date for serializer compatibility)
            result_map = {}
            for key, label, start_dt, end_dt in buckets:
                result_map[key] = {
                    'key': key,
                    'label': label,
                    'date': start_dt.date().isoformat(),  # add date field expected by serializer
                    'revenue': Decimal('0'),
                    'cost': Decimal('0'),
                    'profit': Decimal('0'),
                }

            # Iterate orders and accumulate revenue/cost
            for order in orders_qs:
                order_dt = getattr(order, date_field, None) or order.updated_at
                assigned_key = None
                for key, _, start_dt, end_dt in buckets:
                    if order_dt >= start_dt and order_dt <= end_dt:
                        assigned_key = key
                        break
                if assigned_key is None:
                    # Debug: show first bucket range for comparison
                    if buckets:
                        first_key, _, first_start, first_end = buckets[0]
                        print(f"⚠️ Order {order.id} with {date_field}={order_dt} not in any bucket (first bucket: {first_key} {first_start} to {first_end})")
                    else:
                        print(f"⚠️ Order {order.id} with {date_field}={order_dt} not in any bucket")
                    continue
                print(f"✅ Order {order.id} assigned to bucket {assigned_key}")

                gross = Decimal(str(order.cost_confirm or 0))
                result_map[assigned_key]['revenue'] += gross

                # compute worked_hours and per-employee cost
                estimated_h = float(order.estimated_hours or 0)
                requested_h = float(order.requested_hours or 0)
                if estimated_h > 0 and requested_h > 0:
                    worked_hours = min(estimated_h, requested_h)
                elif estimated_h > 0:
                    worked_hours = estimated_h
                elif requested_h > 0:
                    worked_hours = requested_h
                else:
                    worked_hours = 0.0

                order_emps = list(order.employees.all())
                order_cost = Decimal('0')
                for emp in order_emps:
                    # ensure salary numeric
                    salary = Decimal(str(getattr(emp, 'salary', 0) or 0))
                    order_cost += (salary * Decimal(str(worked_hours)))

                result_map[assigned_key]['cost'] += order_cost

            # Build final_result
            final_result = []
            for key, label, start_dt, _ in buckets:
                item = result_map[key]
                item['profit'] = item['revenue'] - item['cost']
                final_result.append({
                    'period': item['key'],
                    'date': item.get('date') or start_dt.date().isoformat(),
                    'label': label,
                    'revenue': float(item['revenue'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                    'cost': float(item['cost'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                    'profit': float(item['profit'].quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                })

            return final_result

        except Exception as exc:
            # Log full traceback to server console for debugging (don't expose to client)
            print("❌ Error in calculate_revenue_cost_profit:", exc)
            traceback.print_exc()
            return []
