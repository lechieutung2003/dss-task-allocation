from django.urls import re_path, include, path
from rest_framework_nested import routers as drf_nested_routers  # Đổi tên để rõ ràng
from base import routers as base_routers  # Đổi tên để rõ ràng
from .views.register_customer import RegisterCustomerAPIView  # Di chuyển lên đầu
from .views.profile_customer import CustomerProfileAPIView

from .views import (
    GroupViewSet,
    OfficeViewSet,
    HolidayViewSet,
    WorkSessionViewSet,
    UnitViewSet,
    UnitTypeViewSet
)

# Tách riêng imports cho API orders để rõ ràng hơn
from .views.order import OrderViewSet, AssignmentViewSet, CustomerViewSet, ServiceTypeViewSet

app_name = "hr"
router = base_routers.MutipleUpdateRouter(trailing_slash=False)

# Đăng ký các ViewSets
router.register(r'groups', GroupViewSet, basename="groups")
router.register(r'offices', OfficeViewSet, basename="offices")
router.register(r'units', UnitViewSet, basename="units")
router.register(r'unit-types', UnitTypeViewSet, basename="unit-types")

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
    path('api/v1/register-customer', RegisterCustomerAPIView.as_view(), name='register-customer'),
    path('api/v1/me', CustomerProfileAPIView.as_view(), name='profile-customer')
]