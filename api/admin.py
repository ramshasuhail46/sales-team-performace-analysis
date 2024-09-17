from django.contrib import admin
from api.models import SalesData

# Register your models here.


class SalesDataAdmin(admin.ModelAdmin):
    list_display = (
        'employee_name', 'created', 'dated', 'lead_taken', 'tours_booked',
        'applications', 'tours_per_lead', 'apps_per_tour', 'apps_per_lead',
        'revenue_confirmed', 'revenue_pending', 'revenue_runrate',
        'tours_in_pipeline', 'avg_deal_value_30_days', 'avg_close_rate_30_days',
        'estimated_revenue', 'tours', 'tours_runrate', 'tours_scheduled',
        'tours_pending', 'tours_cancelled'
    )
    search_fields = ('employee_name', 'created', 'dated')
    list_filter = ('created', 'dated')


admin.site.register(SalesData, SalesDataAdmin)
