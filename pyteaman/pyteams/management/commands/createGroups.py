from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User


class Command(BaseCommand):
    help = 'Create groups and assign permissions to groups.'

    def handle(self, *args, **options):
        group_names = ['administrator', 'manager', 'member']
        all_groups = []
        for group in group_names:
            all_groups.append(Group.objects.get_or_create(name=group))
        if all_groups:
            for x in all_groups:
                if not x[1]:
                    print '\nGroup {} already exists.\n'.format(x[0])
                else:
                    print 'Group {} created successfully.\n'.format(x[0])