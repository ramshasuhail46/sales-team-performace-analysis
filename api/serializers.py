from rest_framework import serializers
from .models import SalesData

class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
