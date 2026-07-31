from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from analytics.models import Visitor
from projects.models import Project
from blogs.models import Blog
from contact.models import ContactMessage
from skills.models import Skill
from datetime import timedelta
from django.utils import timezone

class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def handle_no_permission(self):
        return redirect('/admin/login/?next=/dashboard/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)

        context['total_visitors'] = Visitor.objects.count()
        context['unique_ips'] = Visitor.objects.values('ip_address').distinct().count()
        context['recent_visitors'] = Visitor.objects.filter(timestamp__gte=thirty_days_ago).count()
        
        context['total_projects'] = Project.objects.count()
        context['top_projects'] = Project.objects.order_by('-views_count')[:5]
        
        context['total_blogs'] = Blog.objects.count()
        context['top_blogs'] = Blog.objects.order_by('-views_count')[:5]
        
        context['contact_messages'] = ContactMessage.objects.all()[:10]
        context['unread_messages_count'] = ContactMessage.objects.filter(is_read=False).count()
        context['total_skills'] = Skill.objects.count()

        return context

@staff_member_required(login_url='/admin/login/?next=/dashboard/')
def analytics_api(request):
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        return JsonResponse({'error': 'Admin Login Required'}, status=403)

    now = timezone.now()
    dates = []
    visit_counts = []

    for i in range(6, -1, -1):
        day = now.date() - timedelta(days=i)
        dates.append(day.strftime('%b %d'))
        count = Visitor.objects.filter(timestamp__date=day).count()
        visit_counts.append(count)

    top_projects = list(Project.objects.values('title', 'views_count').order_by('-views_count')[:5])

    return JsonResponse({
        'traffic_labels': dates,
        'traffic_data': visit_counts,
        'projects': top_projects,
    })
