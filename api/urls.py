from django.urls import path
from .views import FileUploadView, SalesInsightView, RepPerformanceView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('insight/', SalesInsightView.as_view(), name='sales-insight'),
    path('rep_performance/', RepPerformanceView.as_view(), name='rep_performance'),
]
