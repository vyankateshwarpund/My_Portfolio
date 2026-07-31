from django.db import models

class Resume(models.Model):
    title = models.CharField(max_length=150, default='Vyankateshwar Pund - Software Engineer Resume')
    file = models.FileField(upload_to='resume/')
    is_active = models.BooleanField(default=True)
    total_downloads = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Active: {self.is_active})"

class Certificate(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150)
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/pdf/', blank=True, null=True)
    certificate_image = models.ImageField(upload_to='certificates/img/', blank=True, null=True)

    class Meta:
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.title} - {self.issuer}"
