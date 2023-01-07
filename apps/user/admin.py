from django.contrib import admin
from django.contrib.auth.models import Group

from apps.user.models import User, UserFollow

admin.site.register(User)
admin.site.unregister(Group)
admin.site.register(UserFollow)
