from django.contrib import admin

from app.base.models import Hackathon, TeamParticipant, HackathonParticipant, Team, Leaderboard


class LeaderboardAdmin(admin.ModelAdmin):
    model = Leaderboard
    ordering = ('score',)


class HackathonAdmin(admin.ModelAdmin):
    model = Hackathon
    ordering = ('-id',)
    list_display = ('id', 'name', 'start_time', 'end_time')


class TeamAdmin(admin.ModelAdmin):
    model = Team
    ordering = ('-id',)
    list_display = ('id', 'name', 'hackathon', 'url')


# class HackathonParticipantAdmin(admin.ModelAdmin):
#    model = HackathonParticipant
#    ordering = ('-hackathon__id', )
#    list_display = ('user__email', 'hackathon__name')


admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(TeamParticipant)
admin.site.register(HackathonParticipant)
# admin.site.registerHackathonParticipantAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Leaderboard, LeaderboardAdmin)
