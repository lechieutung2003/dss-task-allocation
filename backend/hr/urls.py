from django.urls import re_path, include, path
from rest_framework_nested import routers as drf_nested_routers  
from .views.employee_order import EmployeeOrdersAPIView
from base import routers as base_routers  
from hr.views.customer import RegisterCustomerAPIView, CustomerInfoAPIView  
from hr.views.customer_order import SimpleCreateOrderAPIView
from hr.views.customer_order import CustomerOrdersAPIView, UpdateOrderFeedbackAPIView, UpdateOrderAPIView
from .views import (
    GroupViewSet,
    OfficeViewSet,
    HolidayViewSet,
    WorkSessionViewSet,
    UnitViewSet,
    UnitTypeViewSet,
    SkillViewSet
)

from .views.order import OrderViewSet, AssignmentViewSet, CustomerViewSet, ServiceTypeViewSet,AssignmentViewSet
from .views.dashboard import (
    DashboardOverviewView,
    PriorityOrdersView,
    EmployeeKPIView,
    DailySummaryView,
    DashboardFullView
)
from .views.enhanced_dashboard import (
    PriorityOrdersView as PriorityOrdersEnhancedView,
    EmployeeKPIView as EmployeeKPIEnhancedView,
    EmployeeKPIDetailView,
    RevenueCostProfitView,
    EnhancedDashboardFullView
)

app_name = "hr"
router = base_routers.MutipleUpdateRouter(trailing_slash=False)

# Đăng ký các ViewSets
router.register(r'groups', GroupViewSet, basename="groups")
router.register(r'offices', OfficeViewSet, basename="offices")
router.register(r'units', UnitViewSet, basename="units")
router.register(r'unit-types', UnitTypeViewSet, basename="unit-types")
router.register(r'skills', SkillViewSet, basename="skills")

# Đăng ký các ViewSets liên quan đến order
router.register(r'customers', CustomerViewSet, basename="customers")
router.register(r'service-types', ServiceTypeViewSet, basename="service-types")
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'assignments', AssignmentViewSet, basename="assignments")


# Đăng ký các router lồng nhau
# 1. Đảm bảo đã đăng ký 'groups' trong router chính
group_router = base_routers.NestedMutipleUpdateRouter(router, r'groups', lookup='group')

# 2. Đăng ký 'offices' trong group_router
group_router.register(r'offices', OfficeViewSet, basename="group-offices")

# 3. Sau khi đã đăng ký 'offices' trong group_router, mới đăng ký các child routers
office_router = base_routers.NestedMutipleUpdateRouter(group_router, r'offices', lookup='office')
office_router.register(r'holidays', HolidayViewSet, basename="holidays")
office_router.register(r'work-sessions', WorkSessionViewSet, basename="work-sessions")

# Router cho offices không thuộc group
office_router_non_group = base_routers.NestedMutipleUpdateRouter(router, r'offices', lookup='office')
office_router_non_group.register(r'holidays', HolidayViewSet, basename="non-group-holidays")
office_router_non_group.register(r'work-sessions', WorkSessionViewSet, basename="non-group-work-sessions")

# Định nghĩa URLs
urlpatterns = [
    re_path(r'^api/v1/', include(router.urls)),
    re_path(r'^api/v1/', include(group_router.urls)),
    re_path(r'^api/v1/', include(office_router.urls)),
    re_path(r'^api/v1/', include(office_router_non_group.urls)),  
    path('api/v1/employee-orders', EmployeeOrdersAPIView.as_view(), name='employee-orders'),
    # API customer
    path('api/v1/register-customer', RegisterCustomerAPIView.as_view(), name='register-customer'),
    path('api/v1/customer/info', CustomerInfoAPIView.as_view(), name='customer-info'),
    path('api/v1/customer/orders', CustomerOrdersAPIView.as_view(), name='customer-orders'),
    path('api/v1/customer/orders/<uuid:order_id>', UpdateOrderAPIView.as_view(), name='customer-order-detail'),
    path('api/v1/customer/orders/<uuid:order_id>/feedback', UpdateOrderFeedbackAPIView.as_view(), name='update-order-feedback'),
    path('api/v1/customer/create-order', SimpleCreateOrderAPIView.as_view(), name='simple-create-order'),
    
    # Dashboard API endpoints
    path('api/v1/dashboard/overview', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('api/v1/dashboard/priority-orders', PriorityOrdersView.as_view(), name='dashboard-priority-orders'),
    path('api/v1/dashboard/employee-kpi', EmployeeKPIView.as_view(), name='dashboard-employee-kpi'),
    path('api/v1/dashboard/daily-summary', DailySummaryView.as_view(), name='dashboard-daily-summary'),
    path('api/v1/dashboard/full', DashboardFullView.as_view(), name='dashboard-full'),
    
    # Enhanced Dashboard API endpoints (3 modules)
    path('api/v1/enhanced-dashboard/priority-orders', PriorityOrdersEnhancedView.as_view(), name='enhanced-priority-orders'),
    path('api/v1/enhanced-dashboard/employee-kpi', EmployeeKPIEnhancedView.as_view(), name='enhanced-employee-kpi'),
    path('api/v1/enhanced-dashboard/employee-kpi/<int:employee_id>', EmployeeKPIDetailView.as_view(), name='enhanced-employee-kpi-detail'),
    path('api/v1/enhanced-dashboard/revenue-cost-profit', RevenueCostProfitView.as_view(), name='enhanced-revenue-cost-profit'),
    path('api/v1/enhanced-dashboard/full', EnhancedDashboardFullView.as_view(), name='enhanced-dashboard-full'),
]