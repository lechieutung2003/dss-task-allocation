from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from ..models import Employee
from oauth.models import User, Role
from oauth.serializers import UserShortSerializer, RoleShortSerializer
from .employee_additional_information import EmployeeAdditionalInformationSerializer

class EmployeeSerializer(WritableNestedSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='user')
    office_id = UUIDField(required=False, allow_null=True)
    roles = RoleShortSerializer(many=True, required=False)
    role_ids = serializers.PrimaryKeyRelatedField(required=False, write_only=True, many=True, allow_null=True,
                                                   allow_empty=True,
                                                   queryset=Role.objects.all(),
                                                   source='roles')
    additional_information = EmployeeAdditionalInformationSerializer(many=True, required=False)
    is_currently_active = serializers.SerializerMethodField()
    current_status_text = serializers.SerializerMethodField()
    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'user_id',
            'office_id',
            'first_name',
            'last_name',
            'work_mail',
            'personal_mail',
            'date_of_birth',
            'join_date',
            'phone',
            'gender',
            'avatar',
            'roles',
            'role_ids',
            'additional_information',
            'status',
            'updated_at',
            # Thêm các trường mới
            'area',
            'working_start_time',
            'working_end_time',
            'completed_orders_count',
            'salary',
            'total_hours_worked',
            'is_currently_active',
            'current_status_text'
        ]
        extra_kwargs = {
            'user': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'work_mail': {'required': False},
            'personal_mail': {'required': False},
            'date_of_birth': {'required': False},
            'phone': {'required': False},
            'gender': {'required': False},
            'avatar': {'required': False},
            'roles': {'required': False},
            'status': {'required': False},
            'updated_at': {'read_only': True},
            # Thêm các trường mới
            'area': {'required': False},
            'working_start_time': {'required': False},
            'working_end_time': {'required': False},
            'completed_orders_count': {'required': False},
            'salary': {'required': False},
            'total_hours_worked': {'required': False},
        }
        nested_create_fields = ["user"]
        nested_update_fields = ["additional_information"]
    def get_is_currently_active(self, obj):
        """Check if employee is currently active based on working hours"""
        return self._calculate_current_status(obj)['is_active']
    
    def get_current_status_text(self, obj):
        """Get current status text"""
        return self._calculate_current_status(obj)['status_text']
    
    def _calculate_current_status(self, obj):
        """Calculate current status based on working hours and current time"""
        if not obj.working_start_time or not obj.working_end_time:
            return {
                'is_active': False,
                'status_text': 'No working hours set'
            }
        
        # Get current time in Vietnam timezone (or your local timezone)
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_time = timezone.now().astimezone(vietnam_tz).time()
        
        # Convert working hours to time objects for comparison
        start_time = obj.working_start_time
        end_time = obj.working_end_time
        
        # Check if current time is within working hours
        if start_time <= end_time:
            # Normal case: start time is before end time (same day)
            is_active = start_time <= current_time <= end_time
        else:
            # Handle overnight shifts (start time > end time)
            is_active = current_time >= start_time or current_time <= end_time
        
        # Determine status text
        if is_active:
            status_text = 'Active - Working Hours'
        else:
            if current_time < start_time:
                status_text = f'Offline - Starts at {start_time.strftime("%H:%M")}'
            else:
                status_text = f'Offline - Ended at {end_time.strftime("%H:%M")}'
        
        return {
            'is_active': is_active,
            'status_text': status_text
        }

class EmployeeShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='user')
    class Meta:
        model = Employee
        fields = [
            'id',
            'user',
            'user_id',
            'office_id',
            'first_name',
            'last_name',
            'work_mail',
            'personal_mail',
            'date_of_birth',
            'phone',
            'gender',
            'avatar',
            'status',
            # Thêm các trường mới
            'area',
            'working_start_time',
            'working_end_time',
            'completed_orders_count',
            'salary',
            'total_hours_worked',
        ]
        extra_kwargs = {
            'user': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'work_mail': {'required': False},
            'personal_mail': {'required': False},
            'date_of_birth': {'required': False},
            'phone': {'required': False},
            'gender': {'required': False},
            'avatar': {'required': False},
            'status': {'required': False},
            # Thêm các trường mới
            'area': {'required': False},
            'working_start_time': {'required': False},
            'working_end_time': {'required': False},
            'completed_orders_count': {'required': False},
            'salary': {'required': False},
            'total_hours_worked': {'required': False},
        }