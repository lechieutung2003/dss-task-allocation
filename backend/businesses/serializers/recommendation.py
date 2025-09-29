from rest_framework import serializers
from businesses.models import Employee
from hr.models import  Order

class RecommendationEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 
            'first_name', 
            'last_name',
            'area',
            'skills',
            'working_start_time',
            'working_end_time'
        ]

class RecommendationSerializer(serializers.Serializer):
    employee = RecommendationEmployeeSerializer()
    score = serializers.IntegerField()
    reasons = serializers.ListField(child=serializers.CharField())