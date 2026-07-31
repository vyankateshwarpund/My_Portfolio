from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from .models import Project, ProjectCategory, Technology

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        queryset = Project.objects.all()
        category_slug = self.request.GET.get('category')
        tech_id = self.request.GET.get('tech')
        search_query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tech_id:
            queryset = queryset.filter(tech_stack__id=tech_id)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(short_description__icontains=search_query) |
                Q(full_details__icontains=search_query)
            )
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        context['technologies'] = Technology.objects.all()
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment view counter
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related projects based on category
        context['related_projects'] = Project.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context

def like_project(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.likes_count += 1
        project.save(update_fields=['likes_count'])
        return JsonResponse({'status': 'success', 'likes_count': project.likes_count})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
