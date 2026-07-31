from django.contrib import admin
from .models import ProfileInfo, Experience, Education, Service, Achievement, SocialLink, Testimonial, CareerStep

@admin.register(ProfileInfo)
class ProfileInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'location')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('role', 'company_name', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current', 'start_date')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'end_year', 'cgpa')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'organization', 'date')

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url', 'order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'organization', 'rating')

@admin.register(CareerStep)
class CareerStepAdmin(admin.ModelAdmin):
    list_display = ('year', 'title', 'order')
