"""
Dashboard Views - API endpoints cho admin dashboard
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from datetime import timedelta, datetime

from hr.services.dashboard_service import DashboardService
from hr.serializers.dashboard import (
    PriorityOrderSerializer,
    EmployeeKPISerializer,
    DailySummarySerializer,
    DashboardOverviewSerializer,
    DashboardResponseSerializer
)


class DashboardOverviewView(APIView):
    """
    GET /api/hr/dashboard/overview/
    Lấy tổng quan dashboard (tổng số orders, doanh thu, nhân viên...)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Lấy tổng quan dashboard với các chỉ số tổng hợp",
        responses={
            200: DashboardOverviewSerializer(),
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            overview_data = DashboardService.get_dashboard_overview()
            serializer = DashboardOverviewSerializer(overview_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PriorityOrdersView(APIView):
    """
    GET /api/hr/dashboard/priority-orders/
    Lấy danh sách orders ưu tiên (đã tính priority score)
    Query params:
        - limit: số lượng orders trả về (default: 20)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Lấy danh sách orders ưu tiên với priority score đã tính",
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Số lượng orders trả về",
                type=openapi.TYPE_INTEGER,
                default=20
            )
        ],
        responses={
            200: PriorityOrderSerializer(many=True),
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            limit = int(request.query_params.get('limit', 20))
            priority_orders = DashboardService.get_priority_orders(limit=limit)
            serializer = PriorityOrderSerializer(priority_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmployeeKPIView(APIView):
    """
    GET /api/hr/dashboard/employee-kpi/
    Lấy KPI của tất cả nhân viên (số đơn hoàn thành, completion rate, KPI score...)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Lấy KPI của tất cả nhân viên với các chỉ số đã tính",
        responses={
            200: EmployeeKPISerializer(many=True),
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            employee_kpi = DashboardService.calculate_employee_kpi()
            serializer = EmployeeKPISerializer(employee_kpi, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DailySummaryView(APIView):
    """
    GET /api/hr/dashboard/daily-summary/
    Lấy tổng hợp kinh doanh theo ngày (revenue, cost, profit, số đơn success/fail)
    Query params:
        - start_date: ngày bắt đầu (format: YYYY-MM-DD, default: 30 ngày trước)
        - end_date: ngày kết thúc (format: YYYY-MM-DD, default: hôm nay)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Lấy tổng hợp kinh doanh theo ngày",
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Ngày bắt đầu (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Ngày kết thúc (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            )
        ],
        responses={
            200: DailySummarySerializer(many=True),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            # Parse date params
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(start_date)
            else:
                start_date = timezone.now() - timedelta(days=30)
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(end_date)
            else:
                end_date = timezone.now()
            
            daily_summary = DashboardService.calculate_daily_summary(
                start_date=start_date,
                end_date=end_date
            )
            
            serializer = DailySummarySerializer(daily_summary, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': f'Invalid date format: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardFullView(APIView):
    """
    GET /api/hr/dashboard/full/
    Lấy tất cả dữ liệu dashboard trong 1 request (tổng hợp)
    Query params:
        - order_limit: số lượng priority orders (default: 20)
        - start_date: ngày bắt đầu cho daily summary (YYYY-MM-DD)
        - end_date: ngày kết thúc cho daily summary (YYYY-MM-DD)
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Lấy tất cả dữ liệu dashboard trong một request",
        manual_parameters=[
            openapi.Parameter(
                'order_limit',
                openapi.IN_QUERY,
                description="Số lượng priority orders",
                type=openapi.TYPE_INTEGER,
                default=20
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Ngày bắt đầu cho daily summary (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Ngày kết thúc cho daily summary (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            )
        ],
        responses={
            200: DashboardResponseSerializer(),
            400: "Bad Request",
            500: "Internal Server Error"
        }
    )
    def get(self, request):
        try:
            # Parse params
            order_limit = int(request.query_params.get('order_limit', 20))
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                start_date = timezone.make_aware(start_date)
            else:
                start_date = timezone.now() - timedelta(days=30)
            
            if end_date_str:
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                end_date = timezone.make_aware(end_date)
            else:
                end_date = timezone.now()
            
            # Gather all data
            dashboard_data = {
                'overview': DashboardService.get_dashboard_overview(),
                'priority_orders': DashboardService.get_priority_orders(limit=order_limit),
                'employee_kpi': DashboardService.calculate_employee_kpi(),
                'daily_summary': DashboardService.calculate_daily_summary(
                    start_date=start_date,
                    end_date=end_date
                )
            }
            
            serializer = DashboardResponseSerializer(dashboard_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response(
                {'error': f'Invalid parameter: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
