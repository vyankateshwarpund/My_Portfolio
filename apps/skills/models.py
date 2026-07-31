from django.db import models

class Skill(models.Model):
    CATEGORY_CHOICES = (
        ('Backend', 'Backend Development'),
        ('Frontend', 'Frontend Development'),
        ('Database', 'Databases & ORM'),
        ('Tools', 'Developer Tools & Platforms'),
        ('Concepts', 'Software Concepts & Architecture'),
        ('Soft Skills', 'Soft Skills & Leadership'),
    )
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Backend')
    proficiency_percent = models.IntegerField(default=85, help_text='Value between 0 and 100')
    level_label = models.CharField(max_length=50, default='Expert')
    years_experience = models.CharField(max_length=50, default='2 Years')
    problems_solved = models.CharField(max_length=50, default='120+ Problems')
    projects_count = models.CharField(max_length=50, default='15 Projects')
    icon_class = models.CharField(max_length=100, default='bi bi-code-slash', help_text='Bootstrap or FontAwesome icon class')
    is_featured = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', '-proficiency_percent']

    def __str__(self):
        return f"{self.name} ({self.category} - {self.level_label})"
