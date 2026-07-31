from django.db import models

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    page_url = models.CharField(max_length=500)
    referrer = models.CharField(max_length=500, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Visitor'
        verbose_name_plural = 'Visitors'

    def __str__(self):
        return f"{self.ip_address} - {self.page_url} @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
