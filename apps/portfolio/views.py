from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import ProfileInfo, Experience, Education, Service, Achievement, Testimonial, CareerStep
from skills.models import Skill
from projects.models import Project
from blogs.models import Blog
from resume.models import Certificate, Resume

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_skills'] = Skill.objects.filter(is_featured=True)[:8]
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:6]
        context['experiences'] = Experience.objects.all()[:3]
        context['latest_blogs'] = Blog.objects.filter(is_published=True)[:3]
        context['services'] = Service.objects.all()[:4]
        context['testimonials'] = Testimonial.objects.all()
        context['career_steps'] = CareerStep.objects.all()
        return context

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.all()
        context['education_list'] = Education.objects.all()
        context['achievements'] = Achievement.objects.all()
        context['career_steps'] = CareerStep.objects.all()
        return context

class ServicesView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

class AchievementsView(ListView):
    model = Achievement
    template_name = 'achievements.html'
    context_object_name = 'achievements'

class CertificatesView(ListView):
    model = Certificate
    template_name = 'certificates.html'
    context_object_name = 'certificates'

def global_search(request):
    query = request.GET.get('q', '').strip()
    project_results = []
    blog_results = []
    skill_results = []

    if query:
        project_results = Project.objects.filter(
            Q(title__icontains=query) | Q(short_description__icontains=query) | Q(features__icontains=query)
        )
        blog_results = Blog.objects.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query),
            is_published=True
        )
        skill_results = Skill.objects.filter(name__icontains=query)

    return render(request, 'search_results.html', {
        'query': query,
        'project_results': project_results,
        'blog_results': blog_results,
        'skill_results': skill_results,
    })
