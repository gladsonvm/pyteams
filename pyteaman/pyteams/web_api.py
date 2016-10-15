from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Team
from .permissions import CreateTeamPermission
from .serializers import TeamSerializer, TeamSerializerUpdate


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, CreateTeamPermission)

    def get_queryset(self):
        queryset = Team.objects.filter(Q(created_by=self.request.user) | Q(members__in=[self.request.user])).distinct()
        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        members = request.data['members']
        member_list = list()
        for member in members:
            member_list.append(User.objects.get(username=member['username']).id)
        request.data['members'] = member_list
        serializer = TeamSerializerUpdate(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
