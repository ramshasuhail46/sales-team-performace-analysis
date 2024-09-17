import csv
import json
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import SalesData
from api.serializers import SalesDataSerializer, FileUploadSerializer


class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data['file']

        if file.name.endswith('.csv'):
            return self.handle_csv(file)
        elif file.name.endswith('.json'):
            return self.handle_json(file)
        else:
            return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)

    def handle_csv(self, file):
        try:
            data = file.read().decode('utf-8')
            reader = csv.DictReader(StringIO(data))
            sales_data_instances = []

            for row in reader:
                serializer = SalesDataSerializer(data=row)
                if serializer.is_valid():
                    sales_data_instances.append(serializer.validated_data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create instances
            SalesData.objects.bulk_create(
                [SalesData(**data) for data in sales_data_instances])
            return Response({'message': 'CSV file processed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def handle_json(self, file):
        try:
            data = json.load(file)
            sales_data_instances = []

            for item in data:
                serializer = SalesDataSerializer(data=item)
                if serializer.is_valid():
                    sales_data_instances.append(serializer.validated_data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Bulk create instances
            SalesData.objects.bulk_create(
                [SalesData(**data) for data in sales_data_instances])
            return Response({'message': 'JSON file processed successfully'}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON file'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
