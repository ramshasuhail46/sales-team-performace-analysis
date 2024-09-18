from django.urls import path
from .views import FileUploadView, RepPerformanceView, TeamPerformanceView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='upload_file'),
    path('rep_performance/', RepPerformanceView.as_view(), name='rep_performance'),
    path('team_performance/', TeamPerformanceView.as_view(),
         name='team_performance'),
]
