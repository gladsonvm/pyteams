from rest_framework import serializers
from .models import Team
from django.contrib.auth.models import User


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class TeamSerializerUpdate(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('name', 'description', 'members', 'team_type', 'created_by')


class TeamSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Team
        fields = ('name', 'description', 'members', 'team_type', 'created_by')
