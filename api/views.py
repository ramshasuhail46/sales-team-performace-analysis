# views.py
import csv
import json
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SalesData

class FileUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

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
                sales_data_instances.append(SalesData(
                    employee_name=row.get('employee_name', ''),
                    created=row.get('created', ''),
                    dated=row.get('dated', ''),
                    lead_taken=int(row.get('lead_taken', 0)),
                    tours_booked=int(row.get('tours_booked', 0)),
                    applications=int(row.get('applications', 0)),
                    tours_per_lead=float(row.get('tours_per_lead', 0)),
                    apps_per_tour=float(row.get('apps_per_tour', 0)),
                    apps_per_lead=float(row.get('apps_per_lead', 0)),
                    revenue_confirmed=row.get('revenue_confirmed', '0.00'),
                    revenue_pending=row.get('revenue_pending', '0.00'),
                    revenue_runrate=row.get('revenue_runrate', '0.00'),
                    tours_in_pipeline=int(row.get('tours_in_pipeline', 0)),
                    avg_deal_value_30_days=row.get('avg_deal_value_30_days', '0.00'),
                    avg_close_rate_30_days=float(row.get('avg_close_rate_30_days', 0)),
                    estimated_revenue=row.get('estimated_revenue', '0.00'),
                    tours=int(row.get('tours', 0)),
                    tours_runrate=row.get('tours_runrate', '0.00'),
                    tours_scheduled=int(row.get('tours_scheduled', 0)),
                    tours_pending=int(row.get('tours_pending', 0)),
                    tours_cancelled=int(row.get('tours_cancelled', 0)),
                    mon_text=row.get('mon_text', ''),
                    tue_text=row.get('tue_text', ''),
                    wed_text=row.get('wed_text', ''),
                    thur_text=row.get('thur_text', ''),
                    fri_text=row.get('fri_text', ''),
                    sat_text=row.get('sat_text', ''),
                    sun_text=row.get('sun_text', ''),
                    mon_call=int(row.get('mon_call', 0)),
                    tue_call=int(row.get('tue_call', 0)),
                    wed_call=int(row.get('wed_call', 0)),
                    thur_call=int(row.get('thur_call', 0)),
                    fri_call=int(row.get('fri_call', 0)),
                    sat_call=int(row.get('sat_call', 0)),
                    sun_call=int(row.get('sun_call', 0)),
                ))

            # Bulk create instances
            SalesData.objects.bulk_create(sales_data_instances)
            return Response({'message': 'CSV file processed successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def handle_json(self, file):
        try:
            data = json.load(file)
            sales_data_instances = []

            for item in data:
                sales_data_instances.append(SalesData(
                    employee_name=item.get('employee_name', ''),
                    created=item.get('created', ''),
                    dated=item.get('dated', ''),
                    lead_taken=int(item.get('lead_taken', 0)),
                    tours_booked=int(item.get('tours_booked', 0)),
                    applications=int(item.get('applications', 0)),
                    tours_per_lead=float(item.get('tours_per_lead', 0)),
                    apps_per_tour=float(item.get('apps_per_tour', 0)),
                    apps_per_lead=float(item.get('apps_per_lead', 0)),
                    revenue_confirmed=item.get('revenue_confirmed', '0.00'),
                    revenue_pending=item.get('revenue_pending', '0.00'),
                    revenue_runrate=item.get('revenue_runrate', '0.00'),
                    tours_in_pipeline=int(item.get('tours_in_pipeline', 0)),
                    avg_deal_value_30_days=item.get('avg_deal_value_30_days', '0.00'),
                    avg_close_rate_30_days=float(item.get('avg_close_rate_30_days', 0)),
                    estimated_revenue=item.get('estimated_revenue', '0.00'),
                    tours=int(item.get('tours', 0)),
                    tours_runrate=item.get('tours_runrate', '0.00'),
                    tours_scheduled=int(item.get('tours_scheduled', 0)),
                    tours_pending=int(item.get('tours_pending', 0)),
                    tours_cancelled=int(item.get('tours_cancelled', 0)),
                    mon_text=item.get('mon_text', ''),
                    tue_text=item.get('tue_text', ''),
                    wed_text=item.get('wed_text', ''),
                    thur_text=item.get('thur_text', ''),
                    fri_text=item.get('fri_text', ''),
                    sat_text=item.get('sat_text', ''),
                    sun_text=item.get('sun_text', ''),
                    mon_call=int(item.get('mon_call', 0)),
                    tue_call=int(item.get('tue_call', 0)),
                    wed_call=int(item.get('wed_call', 0)),
                    thur_call=int(item.get('thur_call', 0)),
                    fri_call=int(item.get('fri_call', 0)),
                    sat_call=int(item.get('sat_call', 0)),
                    sun_call=int(item.get('sun_call', 0)),
                ))

            # Bulk create instances
            SalesData.objects.bulk_create(sales_data_instances)
            return Response({'message': 'JSON file processed successfully'}, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON file'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
