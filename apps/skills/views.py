from django.views.generic import ListView
from .models import Skill

class SkillListView(ListView):
    model = Skill
    template_name = 'skills.html'
    context_object_name = 'skills'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_skills = Skill.objects.all()
        context['backend_skills'] = all_skills.filter(category='Backend')
        context['frontend_skills'] = all_skills.filter(category='Frontend')
        context['database_skills'] = all_skills.filter(category='Database')
        context['tools_skills'] = all_skills.filter(category='Tools')
        context['concept_skills'] = all_skills.filter(category='Concepts')
        context['soft_skills'] = all_skills.filter(category='Soft Skills')
        return context
