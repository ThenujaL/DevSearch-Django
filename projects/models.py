from email.policy import default
from typing import Tuple
from django.db import models
import uuid

from users.models import Profile

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    #tag is teh the manyToMany relation. We don't have to declare a intermediate table
    featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
    vote_total = models.IntegerField(default=0, blank=True, null=True)
    vote_ratio = models.IntegerField(default=0, blank=True, null=True)
    demo_link = models.CharField(max_length=2000)
    source_link = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

class Review(models.Model):
    VOTE_TYPE = (
        ('UP', 'Up Vote'),
        ('DOWN', 'Down Vote')
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=VOTE_TYPE, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name