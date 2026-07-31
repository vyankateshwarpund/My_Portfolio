from django.db import models
from django.utils.text import slugify

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'Project Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=100, blank=True, default='bi bi-cpu')

    class Meta:
        verbose_name_plural = 'Technologies'

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    full_details = models.TextField()
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    live_demo_url = models.URLField(blank=True, null=True)
    case_study_url = models.URLField(blank=True, null=True)
    tech_stack = models.ManyToManyField(Technology, related_name='projects')
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, related_name='projects')
    
    # Enhanced SaaS metrics & features
    status_badge = models.CharField(max_length=50, default='Production Ready')
    api_calls_count = models.CharField(max_length=50, default='5000+ API Calls')
    db_tables_count = models.CharField(max_length=50, default='25+ DB Tables')
    apis_count = models.CharField(max_length=50, default='40+ APIs')
    features = models.TextField(help_text='Use newlines or bullet points for key features list')
    
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/screenshots/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Screenshot for {self.project.title}"
