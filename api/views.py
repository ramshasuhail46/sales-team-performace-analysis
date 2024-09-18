import csv
import json
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import SalesData
from api.serializers import RepPerformanceSerializer, SalesDataSerializer, FileUploadSerializer, SalesInsightRequestSerializer
from llm import SalesInsightChat


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


class SalesInsightView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SalesInsightRequestSerializer(data=request.data)
        if serializer.is_valid():
            data_type = serializer.validated_data['data_type']
            input_text = serializer.validated_data['input']
            employee_id = serializer.validated_data['employee_id']

            if data_type == 'individual':
                if not employee_id:
                    return Response({'error': 'Employee ID required for individual insights'}, status=status.HTTP_400_BAD_REQUEST)
                data = SalesData.objects.filter(
                    employee_id=employee_id).values()
                print("data: ", data)
            elif data_type == 'team':
                data = SalesData.objects.all().values()
                print("data: ", data)
            elif data_type == 'organization':
                data = SalesData.objects.all().values()
                print("data: ", data)

            sales_insight_chat = SalesInsightChat()

            try:
                print("data before sending into function: ", data)
                insights = sales_insight_chat.chat(data, data_type, input_text)
                return Response({'insights': insights}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RepPerformanceView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RepPerformanceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rep_id = serializer.validated_data['rep_id']
        try:
            data = SalesData.objects.filter(employee_id=rep_id).values()
            if not data:
                return Response({'error': 'No data found for the given rep_id'}, status=status.HTTP_404_NOT_FOUND)

            sales_insight_chat = SalesInsightChat()

            data_type = 'individual'
            input_text = 'Generate detailed performance analysis and feedback.'
            insights = sales_insight_chat.chat(data, data_type, input_text)

            return Response({'insights': insights}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)