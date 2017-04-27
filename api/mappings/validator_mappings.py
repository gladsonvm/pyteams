from django.contrib.auth.models import User

team_types = (
        ('tech', 'tech'),
        ('management', 'management'),
        ('marketing', 'marketing')
    )
tt = [x[0] for x in team_types]
validator_mappings = {
                'TeamValidator':
                {
                    'create':  {
                                 'name': str,
                                 'description': str,
                                 'created_by': User,
                                 'team_type': tt,
                                }

                }

            }


