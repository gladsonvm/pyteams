from .models import Team
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import update_tracker, get_object_or_None
from .decorators import permission_bypass, set_class_attrs
from django.db import transaction


class TeamHandler(object):

    """
    Class that handles create team and all related functions.
    methods included:
    1. create_team()
    2. retrieve_team()
    3. get_team_on_members()
    """

    def __init__(self, *args, **kwargs):
        """
        Make init accepts all values to mandatory fields of team model
        and set it as class variables. that these data can be accessed through out the class
        :param args: contains all mandatory fields to create a team (name, description, created_by, team_type)
        :param kwargs: a dict in format {'user_identifier': 'value'}. value can be either username or email.
        currently it is either username or email
        """
        self.team_name = args[0] if len(args) else kwargs.get('name', None)
        self.team_type = args[1] if len(args) >= 2 else kwargs.get('team_type', None)
        self.user = args[2] if len(args) >= 3 else kwargs.get('user', None)
        self.description = args[3] if len(args) == 4 else kwargs.get('description', None)
        self.permission_bypass_flag = kwargs.get('permission_flag', None)

    @set_class_attrs
    @permission_bypass
    def create_team(self):
        """
        This method creates a new team. if user corresponding to a given user identifier exists, and
        no team exists with a given name. Use this method with decorators only that fetching user object and
        checking permission in implemented in decorators.
        :return: Team name and status variable as json
        """
        if self.user and self.team_name and self.team_type and self.description:
            existing_teams = Team.objects.filter(name=self.team_name, team_type=self.team_type).count()
            if not existing_teams:
                with transaction.atomic():
                    team = Team.objects.create(name=self.team_name,
                                               team_type=self.team_type,
                                               created_by=self.user,
                                               description=self.description)
                    update_status = update_tracker(team)
                if update_status:
                    return {'status': 200, 'team': team}
                return {'status': 500, 'description': 'Database operation failed.'}

            else:
                return {'status': 409, 'description': 'A team with that name already exists.'}
        return {'status': 400, 'description': 'Provide parameters in the order {},{},{},{}'
                .format('team_name', 'team_type', 'created_by', 'description')}

    @set_class_attrs
    @permission_bypass
    def retrieve_team(self, *args, **kwargs):
        """
        Get all details of a team provided self.user or self.members.if only argument is self.user
        then all teams created by self.user is returned. If members is the only argument, then all teams
        having self.user as a member is returned. If queryset is empty, then proper error message is returned.
        :return: team object
        """

        if self.user and self.members and self.team_name:
            teams = Team.objects.filter(Q(created_by=self.user) & Q(members__in=self.members) &
                                        Q(team_name=self.team_name))
        if self.user and self.members:
            teams = Team.objects.filter(created_by=self.user, members__in=self.members)
        if (self.user and self.team_name) or self.team_name:
            teams = Team.objects.filter(team_name=self.team_name, created_by=self.user)
        if self.members and self.team_name:
            teams = Team.objects.filter(team_name=self.team_name, members__in=self.members)
        if self.user:
            teams = Team.objects.filter(created_by=self.user)
        if self.members:
            teams = Team.objects.filter(members__in=self.members)
        if teams:
            return {'status': 200, 'teams': teams}
        else:
            return {'status': 204, 'description': 'No teams with creator/members matching with args/kwargs found'}

    @set_class_attrs
    @permission_bypass
    def update_team(self):
        """
        This method checks for an existing team object and update the same with arguments provided.
        :return: team if updates else error with appropriate status code.
        """

class CustomException(Exception):
    pass
