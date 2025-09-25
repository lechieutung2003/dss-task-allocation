
from rest_framework import serializers
from hr.models.customer import Customer
from hr.serializers.customer import CustomerProfileSerializer

class CustomerProfileSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["id", "email", "first_name", "last_name", "name", "phone", "address", "area"]

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    def get_first_name(self, obj):
        return obj.user.first_name if obj.user else None

    def get_last_name(self, obj):
        return obj.user.last_name if obj.user else None
