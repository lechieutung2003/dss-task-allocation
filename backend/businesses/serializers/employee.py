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