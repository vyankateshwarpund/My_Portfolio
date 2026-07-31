from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/like/', views.like_project, name='like_project'),
]
