from django.urls import path
from .views import MaintenanceSubmitView, MaintenanceHistoryView

urlpatterns = [
    path('<int:activity_id>/submit/', MaintenanceSubmitView.as_view(), name='maintenance-submit'),
    path('<int:activity_id>/history/', MaintenanceHistoryView.as_view(), name='maintenance-history'),
]