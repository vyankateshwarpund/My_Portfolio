from django.db import models

class GalleryItem(models.Model):
    CATEGORY_CHOICES = (
        ('Projects', 'Projects & Code'),
        ('Certificates', 'Certificates & Credentials'),
        ('Workspace', 'Workspace & Tech Setup'),
        ('Events', 'Events & Hackathons'),
    )
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Projects')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.category})"
