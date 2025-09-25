from rest_framework import serializers
from ..models import Order, Assignment, DecisionLog
<<<<<<< HEAD
from ..models.customer import Customer, ServiceType
from businesses.serializers.employee import EmployeeShortSerializer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = '__all__'
=======
from businesses.serializers.employee import EmployeeShortSerializer
from .customer import CustomerSerializer, ServiceTypeSerializer
>>>>>>> Features/employee-management

class OrderSerializer(serializers.ModelSerializer):
    customer_details = CustomerSerializer(source='customer', read_only=True)
    service_details = ServiceTypeSerializer(source='service_type', read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        
    def to_representation(self, instance):
        try:
            representation = super().to_representation(instance)
            representation['customer_name'] = f"{instance.customer.name}" if instance.customer else ""
            return representation
        except ValueError as e:
            if "badly formed hexadecimal UUID string" in str(e):
                print(f"Lỗi UUID với order ID: {instance.id}")
                # Trả về một representation tạm thời
                return {
                    'id': str(instance.id),
                    'error': 'Dữ liệu không hợp lệ'
                }
            raise e

class AssignmentSerializer(serializers.ModelSerializer):
    employee_details = EmployeeShortSerializer(source='employee', read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'

class DecisionLogSerializer(serializers.ModelSerializer):
    employee_details = EmployeeShortSerializer(source='employee', read_only=True)
    
    class Meta:
        model = DecisionLog
        fields = '__all__'