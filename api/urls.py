from django.urls import path
from .views import FileUploadView, SalesInsightView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('insight/', SalesInsightView.as_view(), name='sales-insight'),
]
