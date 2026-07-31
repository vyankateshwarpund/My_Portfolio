from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
    path('certificates/', views.CertificatesView.as_view(), name='certificates'),
    path('search/', views.global_search, name='global_search'),
]
