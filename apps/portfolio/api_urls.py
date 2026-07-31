from django.urls import path
from . import api_views

urlpatterns = [
    path('profile/', api_views.ProfileInfoAPIView.as_view(), name='api_profile'),
    path('experiences/', api_views.ExperienceListAPIView.as_view(), name='api_experiences'),
    path('education/', api_views.EducationListAPIView.as_view(), name='api_education'),
    path('services/', api_views.ServiceListAPIView.as_view(), name='api_services'),
    path('skills/', api_views.SkillListAPIView.as_view(), name='api_skills'),
    path('projects/', api_views.ProjectListAPIView.as_view(), name='api_projects'),
    path('projects/<slug:slug>/', api_views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
    path('blogs/', api_views.BlogListAPIView.as_view(), name='api_blogs'),
    path('contact/', api_views.ContactCreateAPIView.as_view(), name='api_contact'),
]
