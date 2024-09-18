import csv
import json
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import status
from api.models import SalesData
from api.serializers import PerformanceTrendSerializer, RepPerformanceSerializer, SalesDataSerializer, FileUploadSerializer, SalesInsightRequestSerializer
from llm import SalesInsightChat
from django.db.models.functions import TruncMonth, TruncQuarter


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


class TeamPerformanceView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = SalesData.objects.all()
            sales_insight_chat = SalesInsightChat()

            total_leads = data.aggregate(total_leads=Sum('lead_taken'))[
                'total_leads'] or 0
            total_tours = data.aggregate(total_tours=Sum('tours_booked'))[
                'total_tours'] or 0
            total_revenue = data.aggregate(total_revenue=Sum('revenue_confirmed'))[
                'total_revenue'] or 0

            total_reps = data.values('employee_id').distinct().count()
            average_revenue_per_rep = total_revenue / total_reps if total_reps > 0 else 0

            summary_data = {
                'total_leads': total_leads,
                'total_tours': total_tours,
                'total_revenue': total_revenue,
                'total_representatives': total_reps,
                'average_revenue_per_representative': average_revenue_per_rep,
            }
            data_type = 'team'
            input_text = 'Generate a summary of the sales team’s overall performance.'
            insights = sales_insight_chat.chat(
                summary_data, data_type, input_text)

            return Response({'insights': insights}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PerformanceTrendsView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PerformanceTrendSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        time_period = serializer.validated_data['time_period']
        if time_period not in ['monthly', 'quarterly']:
            return Response({'error': 'Invalid time_period parameter. Must be "monthly" or "quarterly".'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if time_period == 'monthly':
                aggregated_data = SalesData.objects.annotate(
                    period=TruncMonth('dated')
                ).values('period').annotate(
                    total_revenue=Sum('revenue_confirmed'),
                    total_leads=Sum('lead_taken'),
                    total_tours=Sum('tours_booked')
                ).order_by('period')

            elif time_period == 'quarterly':
                aggregated_data = SalesData.objects.annotate(
                    period=TruncQuarter('dated')
                ).values('period').annotate(
                    total_revenue=Sum('revenue_confirmed'),
                    total_leads=Sum('lead_taken'),
                    total_tours=Sum('tours_booked')
                ).order_by('period')

            sales_insight_chat = SalesInsightChat()
            data_type = 'time period'
            input_text = 'Analyze sales data and provide insights and forecasting based on the specified time period.'
            insights = sales_insight_chat.chat(
                aggregated_data, data_type, input_text)

            return Response({'insights': insights}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
