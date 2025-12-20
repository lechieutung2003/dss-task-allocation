"""
Enhanced Dashboard Views - Complete API Endpoints
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime, timedelta, time

def _parse_date_only_start(dt_str):
    if not dt_str:
        return None
    # try full datetime first
    dt = parse_datetime(dt_str)
    if dt:
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    # fallback treat as YYYY-MM-DD
    try:
        d = datetime.strptime(dt_str, "%Y-%m-%d").date()
        dt0 = datetime.combine(d, time.min)  # 00:00:00
        return timezone.make_aware(dt0)
    except Exception:
        return None

def _parse_date_only_end(dt_str):
    if not dt_str:
        return None
    dt = parse_datetime(dt_str)
    if dt:
        return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
    try:
        d = datetime.strptime(dt_str, "%Y-%m-%d").date()
        # end of day inclusive
        dt1 = datetime.combine(d, time(23,59,59,999999))
        return timezone.make_aware(dt1)
    except Exception:
        return None



from hr.services.enhanced_dashboard_service import EnhancedDashboardService
from hr.serializers.enhanced_dashboard import (
    PriorityOrderEnhancedSerializer,
    EmployeeKPIEnhancedSerializer,
    EmployeeKPIDetailSerializer,
    RevenueCostProfitSerializer,
    EnhancedDashboardResponseSerializer
)


# ==================== MODULE 1: PRIORITY ORDERS ====================

class PriorityOrdersView(APIView):
    """
    API lấy top 10 đơn ưu tiên
    Auto-refresh mỗi 30 giây từ frontend
    Pagination: 5 đơn/trang
    """
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    
    @swagger_auto_schema(
    operation_description="Get detailed KPI for a specific employee",
    manual_parameters=[
        openapi.Parameter('employee_id', openapi.IN_PATH, type=openapi.TYPE_STRING, required=True),
    ],
    responses={200: EmployeeKPIDetailSerializer()}
)
    def get(self, request):
        try:
            # Get pagination params
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))
            
            # Get top 10 orders
            priority_orders = EnhancedDashboardService.get_priority_orders_top10()
            
            # Paginate
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_orders = priority_orders[start_idx:end_idx]
            
            serializer = PriorityOrderEnhancedSerializer(paginated_orders, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': len(priority_orders),
                    'total_pages': (len(priority_orders) + page_size - 1) // page_size
                }
            })
            
        except Exception as e:
            print(f"❌ Error in PriorityOrdersView: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== MODULE 2: EMPLOYEE KPI ====================

class EmployeeKPIView(APIView):
    """
    API lấy top 10 nhân viên có KPI cao nhất
    Pagination: 5 nhân viên/trang
    """
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    
    @swagger_auto_schema(
        operation_description="Get top 10 employees by KPI score with pagination (5 per page)",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, default=5),
            openapi.Parameter('period', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['week', 'month'], default='week'),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: EmployeeKPIEnhancedSerializer(many=True)}
    )
    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))
            period = request.query_params.get('period', 'week')
            start_date = _parse_date_only_start(request.GET.get('start_date'))
            end_date = _parse_date_only_end(request.GET.get('end_date'))
            
            # Get top 10 employees
            try:
                employee_kpi = EnhancedDashboardService.calculate_employee_kpi_enhanced(
                    start_date=start_date,
                    end_date=end_date,
                    period=period
                )
            except Exception as e:
                print(f"❌ Error in calculate_employee_kpi_enhanced: {e}")
                import traceback
                traceback.print_exc()
                employee_kpi = []
            
            # Paginate
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            paginated_kpi = employee_kpi[start_idx:end_idx]
            
            serializer = EmployeeKPIEnhancedSerializer(paginated_kpi, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': len(employee_kpi),
                    'total_pages': (len(employee_kpi) + page_size - 1) // page_size
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeKPIDetailView(APIView):
    """
    API lấy chi tiết KPI của 1 nhân viên (cho popup)
    """
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    
    @swagger_auto_schema(
        operation_description="Get detailed KPI for a specific employee",
        manual_parameters=[
            openapi.Parameter('employee_id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('period', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['week', 'month'], default='week'),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: EmployeeKPIDetailSerializer()}
    )
    def get(self, request, employee_id):
        try:
            period = request.query_params.get('period', 'week')
            start_date = _parse_date_only_start(request.GET.get('start_date'))
            end_date = _parse_date_only_end(request.GET.get('end_date'))
            
            kpi_detail = EnhancedDashboardService.get_employee_kpi_detail(
                employee_id,
                start_date=start_date,
                end_date=end_date,
                period=period
            )
            
            if kpi_detail is None:
                return Response({
                    'success': False,
                    'error': 'Employee not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = EmployeeKPIDetailSerializer(kpi_detail)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== MODULE 3: REVENUE - COST - PROFIT ====================

class RevenueCostProfitView(APIView):
    """
    API tính Revenue - Cost - Profit theo thời gian
    Hỗ trợ filter: 7 ngày, 30 ngày, quý, custom
    Aggregate theo: ngày, tuần, tháng
    """
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    
    @swagger_auto_schema(
        operation_description="Get Revenue/Cost/Profit data with time filters",
        manual_parameters=[
            openapi.Parameter(
                'filter',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['7days', '30days', 'quarter', 'custom'],
                default='30days'
            ),
            openapi.Parameter(
                'period',
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                enum=['day', 'week', 'month'],
                default='day'
            ),
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: RevenueCostProfitSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        try:
            period = request.GET.get('period', 'day')
            filter_param = request.GET.get('filter', '')  # keep for meta / fallback

            # Try parse explicit ISO start_date / end_date from query params
            def _parse_iso(dt_str):
                if not dt_str:
                    return None
                dt = parse_datetime(dt_str)
                if dt is None:
                    try:
                        dt = datetime.fromisoformat(dt_str)
                    except Exception:
                        return None
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt)
                return dt

            start_date = _parse_date_only_start(request.GET.get('start_date'))
            end_date = _parse_date_only_end(request.GET.get('end_date'))

            # If not provided, fallback to legacy filter param (for backward compatibility)
            if not start_date or not end_date:
                now = timezone.now()
                if filter_param == '7days':
                    end_date = now
                    start_date = now - timedelta(days=7)
                elif filter_param == '30days':
                    end_date = now
                    start_date = now - timedelta(days=30)
                elif filter_param == 'quarter':
                    end_date = now
                    start_date = now - timedelta(days=90)
                else:
                    # default last 30 days
                    end_date = end_date or now
                    start_date = start_date or (end_date - timedelta(days=30))

            # parse date_field from querystring (default updated_at)
            date_field = request.GET.get('date_field', 'updated_at')

            # Call service with explicit start/end and date_field
            data = EnhancedDashboardService.calculate_revenue_cost_profit(
                start_date=start_date,
                end_date=end_date,
                period=period,
                date_field=date_field
            )
            
            serializer = RevenueCostProfitSerializer(data, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'meta': {
                    'filter': filter_param,
                    'period': period,
                    'start_date': start_date.date().isoformat() if start_date else None,
                    'end_date': end_date.date().isoformat() if end_date else None,
                    'total_records': len(data)
                }
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== COMBINED DASHBOARD ====================

class EnhancedDashboardFullView(APIView):
    """
    API tổng hợp toàn bộ dashboard (cả 3 modules)
    """
    permission_classes = [AllowAny]  # TODO: Change to IsAuthenticated in production
    
    @swagger_auto_schema(
        operation_description="Get complete enhanced dashboard data (all 3 modules)",
        responses={200: EnhancedDashboardResponseSerializer()}
    )
    def get(self, request):
        try:
            # Module 1: Priority Orders (top 10)
            priority_orders = EnhancedDashboardService.get_priority_orders_top10()
            
            # Module 2: Employee KPI (top 10)
            employee_kpi = EnhancedDashboardService.calculate_employee_kpi_enhanced()
            
            # Module 3: Revenue/Cost/Profit (30 days, by day)
            end_date = timezone.now()
            start_date = end_date - timedelta(days=30)
            revenue_cost_profit = EnhancedDashboardService.calculate_revenue_cost_profit(
                start_date=start_date,
                end_date=end_date,
                period='day'
            )
            
            return Response({
                'success': True,
                'data': {
                    'priority_orders': PriorityOrderEnhancedSerializer(priority_orders, many=True).data,
                    'employee_kpi': EmployeeKPIEnhancedSerializer(employee_kpi, many=True).data,
                    'revenue_cost_profit': RevenueCostProfitSerializer(revenue_cost_profit, many=True).data,
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ==================== SERVICE TYPE COUNTS ====================

class ServiceTypeCountsView(APIView):
    """
    API: trả về số lượng orders theo service type (cho pie chart)
    Query params: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), date_field (default 'updated_at')
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Get counts of orders grouped by service type",
        manual_parameters=[
            openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('date_field', openapi.IN_QUERY, type=openapi.TYPE_STRING, default='updated_at'),
        ]
    )
    def get(self, request):
        try:
            start_date = _parse_date_only_start(request.GET.get('start_date'))
            end_date = _parse_date_only_end(request.GET.get('end_date'))
            date_field = request.GET.get('date_field', 'updated_at')

            data = EnhancedDashboardService.get_service_type_counts(start_date=start_date, end_date=end_date, date_field=date_field)
            return Response({'success': True, 'data': data})
        except Exception as e:
            import traceback; traceback.print_exc()
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceStatusCountsView(APIView):
    """
    API: trả về số lượng orders theo status (completed / rejected / other)
    Query params: start_date (YYYY-MM-DD), end_date (YYYY-MM-DD), date_field (default 'updated_at')
    """
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            start_date = _parse_date_only_start(request.GET.get('start_date'))
            end_date = _parse_date_only_end(request.GET.get('end_date'))
            date_field = request.GET.get('date_field', 'updated_at')

            data = EnhancedDashboardService.get_service_status_counts(start_date=start_date, end_date=end_date, date_field=date_field)
            return Response({'success': True, 'data': data})
        except Exception as e:
            import traceback; traceback.print_exc()
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
