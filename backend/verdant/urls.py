from django.urls import path
from .views import CalculateVUView, VUSummaryView

urlpatterns = [
    path('<int:activity_id>/calculate/', CalculateVUView.as_view(), name='calculate-vu'),
    path('summary/', VUSummaryView.as_view(), name='vu-summary'),
]