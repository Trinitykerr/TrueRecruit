from django.contrib import admin
from .models import Player
from .models import Coach, CoachMore, PlayerMore, User
# Register your models here.

admin.site.register(User)
admin.site.register(PlayerMore)
admin.site.register(Player)
admin.site.register(Coach)
admin.site.register(CoachMore)
