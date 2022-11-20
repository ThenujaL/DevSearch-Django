
from django.db import models
from django.contrib.auth.models import User #django user models import
import uuid
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=80, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profile-pics/', default="profile-pics/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)    



class Skills(models.Model):

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.name)

