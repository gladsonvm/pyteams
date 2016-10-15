from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Team(models.Model):
    team_types = (
        ('tech', 'tech'),
        ('management', 'management'),
        ('marketing', 'marketing')
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, blank=True, related_name='members')
    team_type = models.CharField(choices=team_types, max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'team_type',)


class Activity(models.Model):
    priorities = (
        (1, 'high'),
        (2, 'medium'),
        (3, 'low')
    )
    status_choices = (
        (1, 'started'),
        (2, 'progress'),
        (3, 'finished'),
        (4, 'terminated'),
        (5, 'suspended')
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True)
    team = models.ForeignKey(Team)
    priority = models.CharField(choices=priorities, max_length=6)
    status = models.CharField(choices=status_choices, max_length=10)

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    activity = models.ForeignKey(Activity)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True)
    comment = models.TextField()

    def __unicode__(self):
        return self.comment


class Reply(models.Model):
    comment = models.ForeignKey(Comment)
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True)
    reply = models.TextField()

    def __unicode__(self):
        return self.reply


class ModelUpdate(models.Model):
    available_models = (
        (1, 'Address'),
        (2, 'Verification'),
        (3, 'UserProfile'),
        (4, 'Team'),
        (5, 'Activity'),
        (6, 'Comment'),
        (7, 'Reply')
    )
    model_name = models.CharField(choices=available_models, max_length=20)
    remarks = models.TextField()
    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.model_name
