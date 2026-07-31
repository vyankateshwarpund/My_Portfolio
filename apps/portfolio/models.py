from django.db import models

class ProfileInfo(models.Model):
    name = models.CharField(max_length=100, default='Vyankateshwar Santosh Pund')
    title_roles = models.CharField(max_length=255, default='Junior Software Engineer | Python Developer | Django Backend Developer | Python Full Stack Developer')
    location = models.CharField(max_length=100, default='Amravati, Maharashtra, India')
    email = models.EmailField(default='pundvyankateshwar@gmail.com')
    phone = models.CharField(max_length=20, default='+91 8263986554')
    linkedin_url = models.URLField(default='https://linkedin.com/in/vyankateshwar-pund-7a654632b')
    github_url = models.URLField(default='https://github.com/vyankateshwarpund')
    about_summary = models.TextField()
    career_goals = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    
    # Quantitative Stats
    projects_completed_count = models.IntegerField(default=8)
    internships_count = models.IntegerField(default=1)
    github_contributions_count = models.IntegerField(default=600)
    technologies_count = models.IntegerField(default=20)
    hours_coding_count = models.IntegerField(default=500)
    years_experience = models.CharField(max_length=20, default='1+ Years')

    class Meta:
        verbose_name = 'Profile Information'
        verbose_name_plural = 'Profile Information'

    def __str__(self):
        return self.name

class Experience(models.Model):
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=100, default='India')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    responsibilities = models.TextField(help_text='Use bullet points or newlines')
    tech_stack_used = models.CharField(max_length=255, help_text='Comma separated technologies')

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Work Experience'
        verbose_name_plural = 'Work Experiences'

    def __str__(self):
        return f"{self.role} at {self.company_name}"

class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10)
    cgpa = models.CharField(max_length=20, default='8.06')
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-end_year']
        verbose_name = 'Education'
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.degree} - {self.institution}"

class Service(models.Model):
    title = models.CharField(max_length=150)
    icon_class = models.CharField(max_length=100, help_text='Bootstrap or FontAwesome icon class e.g. bi bi-code-slash')
    short_description = models.CharField(max_length=255)
    full_description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Achievement(models.Model):
    CATEGORY_CHOICES = (
        ('Hackathon', 'Hackathon'),
        ('Award', 'Award'),
        ('Coding', 'Coding Platform / Contest'),
        ('Internship', 'Internship'),
        ('Training', 'Training & Workshop'),
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Award')
    organization = models.CharField(max_length=150)
    date = models.DateField(null=True, blank=True)
    description = models.TextField()
    certificate_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.category})"

class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon_class = models.CharField(max_length=50, help_text='e.g., bi bi-github')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.platform

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.IntegerField(default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Testimonial from {self.name}"

class CareerStep(models.Model):
    year = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default='bi bi-check-circle-fill')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'year']

    def __str__(self):
        return f"{self.year} - {self.title}"
