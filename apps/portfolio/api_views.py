from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ProfileInfo, Experience, Education, Service, Achievement
from skills.models import Skill
from projects.models import Project
from blogs.models import Blog
from contact.models import ContactMessage

from .serializers import (
    ProfileInfoSerializer, ExperienceSerializer, EducationSerializer, 
    ServiceSerializer, AchievementSerializer
)
from skills.serializers import SkillSerializer
from projects.serializers import ProjectSerializer
from blogs.serializers import BlogSerializer
from contact.serializers import ContactMessageSerializer

class ProfileInfoAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileInfoSerializer

    def get_object(self):
        return ProfileInfo.objects.first()

class ExperienceListAPIView(generics.ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class EducationListAPIView(generics.ListAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class SkillListAPIView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filterset_fields = ['category', 'is_featured']

class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.filter(is_published=True)
    serializer_class = BlogSerializer

class ContactCreateAPIView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
