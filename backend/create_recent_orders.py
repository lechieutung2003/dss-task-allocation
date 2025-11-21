import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from hr.models import Order, ServiceType, Customer

# Get existing data
customers = list(Customer.objects.all()[:5])
service_types = list(ServiceType.objects.all()[:3])

if not customers:
    print("❌ No customers found. Please create customers first.")
    exit(1)

if not service_types:
    print("❌ No service types found. Please create service types first.")
    exit(1)

print(f"Found {len(customers)} customers and {len(service_types)} service types")

# Create 30 orders in the last 30 days
now = datetime.now()
statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'rejected']
created_count = 0

for i in range(30):
    # Random day in the last 30 days
    days_ago = random.randint(0, 29)
    order_date = now - timedelta(days=days_ago)
    
    # Random time in the day
    start_hour = random.randint(6, 20)
    duration = random.randint(1, 8)
    
    preferred_start = order_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    preferred_end = preferred_start + timedelta(hours=duration)
    
    # Random area and cost
    area = random.randint(20, 200)
    cost_per_m2 = random.randint(30, 100) * 1000
    cost = area * cost_per_m2
    
    order = Order.objects.create(
        customer=random.choice(customers),
        service_type=random.choice(service_types),
        preferred_start_time=preferred_start,
        preferred_end_time=preferred_end,
        area_m2=Decimal(str(area)),
        requested_hours=Decimal(str(duration)),
        cost_confirm=Decimal(str(cost)),
        estimated_hours=Decimal(str(duration)),
        status=random.choice(statuses),
        note=f"Order {order_date.strftime('%d/%m/%Y')}"
    )
    created_count += 1
    print(f"✅ Created order {created_count}: {preferred_start.strftime('%d/%m/%Y %H:%M')} - {cost:,}đ - {order.status}")

print(f"\n🎉 Successfully created {created_count} orders in the last 30 days!")
