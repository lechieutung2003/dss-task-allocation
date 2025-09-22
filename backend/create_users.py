import os
import sys
import django

# Thiết lập môi trường Django TRƯỚC KHI import models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

# Chỉ import models SAU KHI đã thiết lập Django
from django.core.management.base import BaseCommand
from oauth.models import User, Role
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Tạo các loại user: SuperAdministrator, Employee, và Guest'

    def handle(self, *args, **options):
        # Tạo SuperAdministrator
        super_admin, created = User.objects.update_or_create(
            email="admin@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "Super",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
                "is_guest": False,
                "active": True
            }
        )
        self.stdout.write(
            self.style.SUCCESS(f"SuperAdministrator {'đã tạo' if created else 'đã cập nhật'} với ID: {super_admin.id}")
        )

        # Tạo Employee
        employee, created = User.objects.update_or_create(
            email="employee@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "New",
                "last_name": "Employee",
                "is_staff": True,
                "is_superuser": False,
                "is_guest": False,
                "active": True
            }
        )
        self.stdout.write(
            self.style.SUCCESS(f"Employee {'đã tạo' if created else 'đã cập nhật'} với ID: {employee.id}")
        )

        # Tạo Guest
        guest, created = User.objects.update_or_create(
            email="guest@gmail.com",
            defaults={
                "password": make_password("123456"),
                "first_name": "Guest",
                "last_name": "User",
                "is_staff": False,
                "is_superuser": False,
                "is_guest": True,
                "active": True
            }
        )
        self.stdout.write(
            self.style.SUCCESS(f"Guest {'đã tạo' if created else 'đã cập nhật'} với ID: {guest.id}")
        )
        
if __name__ == "__main__":
    command = Command()
    command.handle()