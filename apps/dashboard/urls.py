from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='admin_dashboard'),
    path('api/stats/', views.analytics_api, name='dashboard_analytics_api'),
]
