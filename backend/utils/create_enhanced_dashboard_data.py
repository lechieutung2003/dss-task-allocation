import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.utils import timezone
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

# Create orders with different statuses for testing Enhanced Dashboard
now = timezone.now()
statuses = ['pending', 'in_progress', 'completed']
created_count = 0

# 1. Create URGENT orders (1-2 hours from now) - for Priority Orders module
for i in range(5):
    hours_ahead = random.uniform(1.1, 1.9)  # 1-2 hours
    start_time = now + timedelta(hours=hours_ahead)
    duration = random.randint(2, 4)
    end_time = start_time + timedelta(hours=duration)
    
    area = random.randint(30, 150)
    price = random.randint(1500000, 3000000)
    
    order = Order.objects.create(
        customer=random.choice(customers),
        service_type=random.choice(service_types),
        preferred_start_time=start_time,
        preferred_end_time=end_time,
        area_m2=Decimal(str(area)),
        requested_hours=Decimal(str(duration)),
        cost_confirm=Decimal(str(price)),
        estimated_hours=Decimal(str(duration)),
        status='pending',
        note=f"URGENT Order - {hours_ahead:.1f}h from now"
    )
    created_count += 1
    print(f"✅ Created URGENT order {created_count}: {start_time.strftime('%H:%M')} - {price:,}đ - pending")

# 2. Create HIGH PRIORITY orders (2-5 hours from now)
for i in range(10):
    hours_ahead = random.uniform(2.1, 4.9)
    start_time = now + timedelta(hours=hours_ahead)
    duration = random.randint(2, 6)
    end_time = start_time + timedelta(hours=duration)
    
    area = random.randint(30, 200)
    price = random.randint(1000000, 2500000)
    
    order = Order.objects.create(
        customer=random.choice(customers),
        service_type=random.choice(service_types),
        preferred_start_time=start_time,
        preferred_end_time=end_time,
        area_m2=Decimal(str(area)),
        requested_hours=Decimal(str(duration)),
        cost_confirm=Decimal(str(price)),
        estimated_hours=Decimal(str(duration)),
        status=random.choice(['pending', 'in_progress']),
        note=f"High Priority - {hours_ahead:.1f}h from now"
    )
    created_count += 1
    print(f"✅ Created HIGH order {created_count}: {start_time.strftime('%H:%M')} - {price:,}đ - {order.status}")

# 3. Create MEDIUM PRIORITY orders (5-12 hours from now)
for i in range(10):
    hours_ahead = random.uniform(5.1, 11.9)
    start_time = now + timedelta(hours=hours_ahead)
    duration = random.randint(2, 8)
    end_time = start_time + timedelta(hours=duration)
    
    area = random.randint(20, 180)
    price = random.randint(800000, 2000000)
    
    order = Order.objects.create(
        customer=random.choice(customers),
        service_type=random.choice(service_types),
        preferred_start_time=start_time,
        preferred_end_time=end_time,
        area_m2=Decimal(str(area)),
        requested_hours=Decimal(str(duration)),
        cost_confirm=Decimal(str(price)),
        estimated_hours=Decimal(str(duration)),
        status=random.choice(['pending', 'in_progress']),
        note=f"Medium Priority - {hours_ahead:.1f}h from now"
    )
    created_count += 1
    print(f"✅ Created MEDIUM order {created_count}: {start_time.strftime('%H:%M')} - {price:,}đ - {order.status}")

# 4. Create COMPLETED orders (for Revenue/Cost/Profit module)
for i in range(20):
    days_ago = random.randint(1, 25)
    order_date = now - timedelta(days=days_ago)
    
    start_hour = random.randint(6, 18)
    start_time = order_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    duration = random.randint(2, 8)
    end_time = start_time + timedelta(hours=duration)
    
    area = random.randint(30, 200)
    price = random.randint(1000000, 3500000)
    
    order = Order.objects.create(
        customer=random.choice(customers),
        service_type=random.choice(service_types),
        preferred_start_time=start_time,
        preferred_end_time=end_time,
        area_m2=Decimal(str(area)),
        requested_hours=Decimal(str(duration)),
        cost_confirm=Decimal(str(price)),
        estimated_hours=Decimal(str(duration)),
        status='completed',
        note=f"Completed {days_ago} days ago"
    )
    # Set updated_at to simulate completion time
    order.updated_at = end_time + timedelta(hours=random.randint(-1, 2))
    order.save()
    
    created_count += 1
    print(f"✅ Created COMPLETED order {created_count}: {order_date.strftime('%d/%m')} - {price:,}đ - completed")

print(f"\n🎉 Successfully created {created_count} orders for Enhanced Dashboard testing!")
print(f"   - 5 URGENT orders (1-2h)")
print(f"   - 10 HIGH priority orders (2-5h)")
print(f"   - 10 MEDIUM priority orders (5-12h)")
print(f"   - 20 COMPLETED orders (last 25 days)")
