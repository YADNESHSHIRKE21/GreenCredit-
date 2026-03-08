from django.urls import path
from .views import VerifyActivityView, VerificationStatusView

urlpatterns = [
    path('<int:activity_id>/verify/', VerifyActivityView.as_view(), name='verify-activity'),
    path('<int:activity_id>/status/', VerificationStatusView.as_view(), name='verification-status'),
]