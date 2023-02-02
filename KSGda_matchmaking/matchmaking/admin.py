from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Player)
admin.site.register(PlayerRating)
admin.site.register(MatchPlayersRating)
admin.site.register(PlayerMatchRateDone)
admin.site.register(Promoter)
admin.site.register(Match)
admin.site.register(Comments)
admin.site.register(Ticket)
admin.site.register(Reserves)
admin.site.register(ReservesPlayer)