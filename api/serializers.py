from rest_framework import serializers
from .models import SalesData


class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class SalesInsightRequestSerializer(serializers.Serializer):
    data_type = serializers.ChoiceField(
        choices=['individual', 'team', 'organization'])
    input = serializers.CharField()
    employee_id = serializers.CharField(required=False)


class RepPerformanceSerializer(serializers.Serializer):
    rep_id = serializers.CharField(required=True)


class PerformanceTrendSerializer(serializers.Serializer):
    time_period = serializers.CharField()
