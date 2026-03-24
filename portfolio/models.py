from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profiles/', blank=True)

    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    email = models.EmailField(blank=True)

    template = models.CharField(max_length=50, default='template1')
    def __str__(self):
        return self.user.username


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    college = models.CharField(max_length=200)
    year = models.CharField(max_length=10)

    def __str__(self):
        return self.degree


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name