from .models import Team
from django.contrib.auth.models import User
from django.db.models import Q
from .utils import update_tracker, get_object_or_None, get_user_on_user_identifier
from .decorators import permission_bypass
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
        self.description = args[1] if len(args) >= 2 else kwargs.get('description', None)
        self.team_type = args[2] if len(args) >= 3 else kwargs.get('team_type', None)
        self.user = args[3] if len(args) == 4 else kwargs.get('user', None)
        self.permission_bypass_flag = kwargs.get('permission_flag', None)

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

    def retrieve_team(self, username=None, **kwargs):
        """
        Get all details of team. Accepts a list of username/email as args.
        list can contain either username or email
        If multiple items are found in list, only those teams having all users corresponding
        to items in the list will be returned
        :return: team object
        """
        if username:
            user_identifier = username.strip(' ')
            if len(user_identifier) and kwargs.get('members', None):
                return self.get_team_on_members(kwargs['members'], user_identifier)
            if len(user_identifier):
                teams = Team.objects.filter(Q(created_by__username=user_identifier) | Q(created_by__email=user_identifier))
                if len(teams):
                    return {'status': 200, 'teams': teams}
                else:
                    return {'status': 204, 'description': 'No team exists with creator as given user identifier.'}
        if kwargs['members']:
            return self.get_team_on_members(kwargs['members'])

    def get_team_on_members(self, members, user_identifier=None):
        """
        return queryset of team model if members in members or user_identifier
        in created_by__username or created_by__email of Team model.
        :param members: a list of username or email that corresponds to user objects
        :param user_identifier: a string that corresponds to username or email field of User model
        :return: Queryset of team if match is found. else json with error code and description
        """
        user_list = []
        if len(members):
            for member in members:
                user = get_object_or_None(User, username=member)
                if user is None:
                    user = get_object_or_None(User, email=member)
                if user:
                    user_list.append(user)
        if user_identifier and len(user_list):
            teams = Team.objects.filter(
                Q(created_by__username=user_identifier) | Q(created_by__email=user_identifier) &
                Q(members__in=user_list)
            )
        if len(user_list):
            teams = Team.objects.filter(members__in=user_list)
        else:
            return {'status': 204, 'description': 'No users with the given identifiers exist.'}
        return {'status': 200, 'teams': teams}


class CustomException(Exception):
    pass
