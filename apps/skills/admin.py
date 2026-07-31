from django.contrib import admin
from .models import Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_percent', 'is_featured', 'order')
    list_filter = ('category', 'is_featured')
    search_fields = ('name',)
