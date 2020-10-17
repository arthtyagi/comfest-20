from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import validate_image_file_extension
from django.urls import reverse_lazy
from django.utils.text import slugify

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(
        null = True,
        blank = True,
        default = 'default_user.jpg',
        upload_to = "profile_pics/",
        validators = [validate_image_file_extension],
        )
    about = models.CharField(null=True, blank=True, max_length=200)
    githubusername = models.CharField(null=True, blank=True, max_length=80)
    community_points = models.IntegerField(default=0)
    slug = models.SlugField(null=True, unique=True, max_length=256)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_absolute_url(self):
        return reverse_lazy("users:profilepage", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        username = self.user.username
        self.slug = slugify(username)
        super().save(*args, **kwargs)
    