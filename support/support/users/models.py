from django.db import models
from django.core.validators import validate_image_file_extension
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True,
                              blank=True,
                              default='default.jpg',
                              upload_to='profile_pics/',
                              validators=[validate_image_file_extension])
    about = models.CharField(null=True, blank=True, max_length=200)
    points = models.IntegerField(default=0)
    followers = models.ManyToManyField(User,
                                       default=None,
                                       blank=True,
                                       related_name="profile_followers")
    slug = models.SlugField(null=True, unique=True, max_length=256)

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse_lazy('users:profilepage', kwargs={'slug': self.slug})

    def followers_as_flat_user_id_list(self):
        return self.followers.values_list('id', flat=True)

    def save(self, *args, **kwargs):
        username = self.user.username
        self.slug = slugify(username)
        super().save(*args, **kwargs)
