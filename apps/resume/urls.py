from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResumeView.as_view(), name='resume'),
    path('download/<int:pk>/', views.download_resume, name='download_resume'),
]
