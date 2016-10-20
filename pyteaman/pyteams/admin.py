from django.contrib import admin
from .models import Team, Activity, Comment, Reply, UpdateTracker

admin.site.register(Team)
admin.site.register(Activity)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(UpdateTracker)