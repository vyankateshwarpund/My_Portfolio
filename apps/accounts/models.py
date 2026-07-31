from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role_title = models.CharField(max_length=100, default='Software Engineer Recruiter / Visitor')

    def __str__(self):
        return f"{self.user.username}'s profile"
