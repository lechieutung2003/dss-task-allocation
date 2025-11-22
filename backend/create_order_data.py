import os
import django
import random
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.timezone import localtime
# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from hr.models import Order, ServiceType, Customer

# ===============================
# CONFIG
# ===============================
NUM_CUSTOMERS = 5
NUM_SERVICES = 2
ORDERS_2024 = 10
ORDERS_2025 = 10

DEFAULT_PRICE_PER_M2 = Decimal('40000')
DEFAULT_CLEAN_RATE = Decimal('20')

STATUS = ['pending', 'confirmed', 'in_progress', 'completed', 'rejected']


def random_datetime_in_month(year, month):
    """Sinh thời gian hợp lệ trong tháng đó."""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    days = (next_month - datetime(year, month, 1)).days

    day = random.randint(1, days)
    hour = random.randint(8, 17)
    minute = random.randint(0, 59)

    return datetime(year, month, day, hour, minute)


# ===============================
# Tạo customers
# ===============================
customers = list(Customer.objects.all())
while len(customers) < NUM_CUSTOMERS:
    c = Customer.objects.create(
        name=f"Khách hàng {len(customers)+1}",
        phone=f"09{random.randint(1000000, 9999999)}",
        address=f"Địa chỉ {len(customers)+1}"
    )
    customers.append(c)

# ===============================
# Tạo services
# ===============================
services = list(ServiceType.objects.all())
while len(services) < NUM_SERVICES:
    s = ServiceType.objects.create(
        name=f"Dịch vụ {len(services)+1}",
        price_per_m2=DEFAULT_PRICE_PER_M2,
        cleaning_rate_m2_per_h=DEFAULT_CLEAN_RATE,
    )
    services.append(s)

# ===============================
# Tạo đơn cho năm 2024
# ===============================
print("⏳ Tạo 10 đơn năm 2024...")

months_2024 = random.sample(range(1, 13), ORDERS_2024)

for month in months_2024:
    created_at = random_datetime_in_month(2024, month)

    cust = random.choice(customers)
    svc = random.choice(services)

    area_m2 = Decimal(random.randint(20, 200))
    est_hours = (area_m2 / svc.cleaning_rate_m2_per_h).quantize(Decimal('0.1'))
    cost = (area_m2 * svc.price_per_m2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    start = created_at + timedelta(hours=random.randint(2, 10))
    end = start + timedelta(hours=float(est_hours))

    order = Order.objects.create(
        customer=cust,
        service_type=svc,
        area_m2=area_m2,
        requested_hours=est_hours,
        preferred_start_time=start,
        preferred_end_time=end,
        estimated_hours=est_hours,
        cost_confirm=cost,
        status=random.choice(STATUS),
        note="Đơn hàng năm 2024"
    )

    Order.objects.filter(id=order.id).update(created_at=created_at)

# ===============================
# Tạo đơn cho năm 2025
# ===============================
print("⏳ Tạo 10 đơn năm 2025...")

months_2025 = random.sample(
    range(1, min(12, timezone.localtime().month) + 1), ORDERS_2025
)

for month in months_2025:
    created_at = random_datetime_in_month(2025, month)

    cust = random.choice(customers)
    svc = random.choice(services)

    area_m2 = Decimal(random.randint(20, 200))
    est_hours = (area_m2 / svc.cleaning_rate_m2_per_h).quantize(Decimal('0.1'))
    cost = (area_m2 * svc.price_per_m2).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    start = created_at + timedelta(hours=random.randint(2, 10))
    end = start + timedelta(hours=float(est_hours))

    order = Order.objects.create(
        customer=cust,
        service_type=svc,
        area_m2=area_m2,
        requested_hours=est_hours,
        preferred_start_time=start,
        preferred_end_time=end,
        estimated_hours=est_hours,
        cost_confirm=cost,
        status=random.choice(STATUS),
        note="Đơn hàng năm 2025"
    )

    Order.objects.filter(id=order.id).update(created_at=created_at)

print("🎉 DONE! Đã tạo 10 đơn năm 2024 + 10 đơn năm 2025.")
