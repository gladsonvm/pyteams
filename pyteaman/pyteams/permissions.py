from rest_framework import permissions

def is_admin_or_manager(user):
    """
    Check if a user belong to either manager or administrator group
    :param user:
    :return: True if user belong to manager/admin group else False
    """
    subscribed_groups = user.groups.all().values_list('name', flat=True)
    if 'administrator' in subscribed_groups or 'manager' in subscribed_groups:
        return True
    return False


class CreateTeamPermission(permissions.BasePermission):
    """
    Check if logged in user belongs to user/admin group for REST api.
    """
    message = 'Adding Members to team not allowed.'

    def has_permission(self, request, view):
        if request.method != 'GET':
            return is_admin_or_manager(request.user)
        return True
