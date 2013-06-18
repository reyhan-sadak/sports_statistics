from django.contrib import admin
from statistics.models import Country, FootballTeam, FootballPlayer, DomesticLeague, DomesticSeason, FootballStadium, FootballManager, DomesticSeasonMatch, MatchGoal

class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name', ]

class FootballTeamAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['league__country', 'league',]

class FootballPlayerAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['team_playing', 'playing_position']

class DomesticLeagueAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['country',]

class DomesticSeasonAdmin(admin.ModelAdmin):
    search_fields = ['league',]
    list_filter = ['league', 'year']

class FootballStadiumAdmin(admin.ModelAdmin):
    search_fields = ['name',]

class FootballManagerAdmin(admin.ModelAdmin):
    search_fields = ['name',]

class DomesticSeasonMatchAdmin(admin.ModelAdmin):
    search_fields = ['homeTeam', 'awayTeam', 'week',]
    list_filter = ['season', 'homeTeam', 'awayTeam',]
    list_display = ('__str__', 'homeGoals', 'awayGoals', 'isFinished',)

class MatchGoalAdmin(admin.ModelAdmin):
    search_fields = ['match', 'player', 'team',]
    list_filter = ['match__season__league', 'match__season', 'player', 'team', 'isOwnGoal',]

admin.site.register(Country, CountryAdmin)
admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballPlayer, FootballPlayerAdmin)
admin.site.register(DomesticLeague, DomesticLeagueAdmin)
admin.site.register(DomesticSeason, DomesticSeasonAdmin)
admin.site.register(FootballStadium, FootballStadiumAdmin)
admin.site.register(FootballManager, FootballManagerAdmin)
admin.site.register(DomesticSeasonMatch, DomesticSeasonMatchAdmin)
admin.site.register(MatchGoal, MatchGoalAdmin)