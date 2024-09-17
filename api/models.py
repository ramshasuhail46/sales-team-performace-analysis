from django.db import models

# Create your models here.


class SalesData(models.Model):
    employee_name = models.CharField(max_length=255)
    created = models.DateTimeField()
    dated = models.DateField()
    lead_taken = models.IntegerField()
    tours_booked = models.IntegerField()
    applications = models.IntegerField()
    tours_per_lead = models.FloatField()
    apps_per_tour = models.FloatField()
    apps_per_lead = models.FloatField()
    revenue_confirmed = models.DecimalField(max_digits=10, decimal_places=2)
    revenue_pending = models.DecimalField(max_digits=10, decimal_places=2)
    revenue_runrate = models.DecimalField(max_digits=10, decimal_places=2)
    tours_in_pipeline = models.IntegerField()
    avg_deal_value_30_days = models.DecimalField(
        max_digits=10, decimal_places=2)
    avg_close_rate_30_days = models.FloatField()
    estimated_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    tours = models.IntegerField()
    tours_runrate = models.DecimalField(max_digits=10, decimal_places=2)
    tours_scheduled = models.IntegerField()
    tours_pending = models.IntegerField()
    tours_cancelled = models.IntegerField()

    mon_text = models.TextField(blank=True, null=True)
    tue_text = models.TextField(blank=True, null=True)
    wed_text = models.TextField(blank=True, null=True)
    thur_text = models.TextField(blank=True, null=True)
    fri_text = models.TextField(blank=True, null=True)
    sat_text = models.TextField(blank=True, null=True)
    sun_text = models.TextField(blank=True, null=True)

    mon_call = models.IntegerField()
    tue_call = models.IntegerField()
    wed_call = models.IntegerField()
    thur_call = models.IntegerField()
    fri_call = models.IntegerField()
    sat_call = models.IntegerField()
    sun_call = models.IntegerField()

    def __str__(self):
        return f"{self.employee_name} - {self.dated}"
