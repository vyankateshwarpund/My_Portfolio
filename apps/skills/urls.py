from django.urls import path
from . import views

urlpatterns = [
    path('', views.SkillListView.as_view(), name='skills_list'),
]
