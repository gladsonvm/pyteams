from django.forms import ModelForm
from core.models import Team


class TeamCreateForm(ModelForm):

    def save(self, commit=True):
        """
        overriding default save() to fetch and save a foreignkey entry.
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.created_by = self.data['created_by']
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m
        return self.instance

    save.alters_data = True

    class Meta:
        model = Team
        fields = ['name', 'description', 'team_type', 'members']
