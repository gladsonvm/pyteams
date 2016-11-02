from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Team(models.Model):
    """
    Team model.
    holds following data for a team object:
    name: name of team.
    description: team description.
    created_by: user (object) who created team.
    created_on: timestamp when the team object is created.
    updated_on: timestamp of last update done to a team object.
    members: list of members (auth.models.user objects) who have joined team.
    team_type = type of team.
    """
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
        permissions = (("edit_members", "Can add or remove members"),)


class Task(models.Model):
    """
    This model saves all info of tasks that are assigned within members of a team.
    """
    team = models.ForeignKey(Team)
    assignor = models.ForeignKey(User, related_name='assignor')
    assignee = models.ForeignKey(User, related_name='assignee')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_created=True)

    def __unicode__(self):
        return self.title


class Activity(models.Model):
    """
    Activity model saves activities involving multiple teams. A typical example is a release event.
    """
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
    team = models.ManyToManyField(Team)
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


class UpdateTracker(models.Model):
    """
    This model tracks each and every updates that is done to a table.
    An object of UpdateTracker is created whenever any model is created or updated.
    """
    available_models = (
        ('team', 'Team'),
        ('activity', 'Activity'),
        ('comment', 'Comment'),
        ('reply', 'Reply'),
    )
    action_choices = (
        ('create', 'create'),
        ('update', 'update'),
        ('update', 'delete'),
    )
    model_name = models.CharField(choices=available_models, max_length=8)
    model_id = models.IntegerField()
    action = models.CharField(choices=action_choices, max_length=10)
    updated_on = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=Team, blank=True)
    updated_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.model_name + self.model_id
