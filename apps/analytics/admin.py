from django.contrib import admin
from .models import Visitor

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'page_url', 'referrer', 'timestamp')
    list_filter = ('timestamp', 'page_url')
    search_fields = ('ip_address', 'page_url', 'user_agent')
