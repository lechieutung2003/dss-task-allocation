"""
Enhanced Dashboard Views - Complete API Endpoints
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import datetime, timedelta



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
        ],
        responses={200: EmployeeKPIEnhancedSerializer(many=True)}
    )
    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))
            
            # Get top 10 employees
            try:
                employee_kpi = EnhancedDashboardService.calculate_employee_kpi_enhanced()
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
        ],
        responses={200: EmployeeKPIDetailSerializer()}
    )
    def get(self, request, employee_id):
        try:
            kpi_detail = EnhancedDashboardService.get_employee_kpi_detail(employee_id)
            
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
    def get(self, request):
        try:
            # Get filter params
            filter_type = request.query_params.get('filter', '30days')
            period = request.query_params.get('period', 'day')
            
            # Calculate date range
            end_date = timezone.now()
            
            if filter_type == '7days':
                start_date = end_date - timedelta(days=7)
            elif filter_type == '30days':
                start_date = end_date - timedelta(days=30)
            elif filter_type == 'quarter':
                start_date = end_date - timedelta(days=90)
            elif filter_type == 'custom':
                # Custom date range
                start_date_str = request.query_params.get('start_date')
                end_date_str = request.query_params.get('end_date')
                
                if start_date_str:
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                    start_date = timezone.make_aware(start_date)
                else:
                    start_date = end_date - timedelta(days=30)
                
                if end_date_str:
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                    end_date = timezone.make_aware(end_date)
            else:
                start_date = end_date - timedelta(days=30)
            
            # Get data
            data = EnhancedDashboardService.calculate_revenue_cost_profit(
                start_date=start_date,
                end_date=end_date,
                period=period
            )
            
            serializer = RevenueCostProfitSerializer(data, many=True)
            
            return Response({
                'success': True,
                'data': serializer.data,
                'meta': {
                    'filter': filter_type,
                    'period': period,
                    'start_date': start_date.date().isoformat(),
                    'end_date': end_date.date().isoformat(),
                    'total_records': len(data)
                }
            })
            
        except Exception as e:
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
