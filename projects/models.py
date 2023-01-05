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
    demo_link = models.CharField(null=True, blank=True, max_length=2000)
    source_link = models.CharField(null=True, blank=True, max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    
    class Meta:
            ordering = ['-vote_ratio', '-vote_total', 'created']

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    #property decorator lets this method be called a property as opposed to a method
    @property
    def get_voteCount(self):
        upVotes = self.review_set.filter(value='UP').count()
        totalVotes = self.review_set.count()

        if totalVotes > 0:
            ratio = int((upVotes / totalVotes) * 100)
        else:
            ratio = 0

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    

class Review(models.Model):
    VOTE_TYPE = (
        ('UP', 'Up Vote'),
        ('DOWN', 'Down Vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True) #null = True for debugging
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(choices=VOTE_TYPE, max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False)
    
    class Meta:
        # enforces that only one comment can be lest per user per project
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name