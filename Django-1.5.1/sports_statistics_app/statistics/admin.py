from django.contrib import admin
from statistics.models import FootballTeam, FootballPlayer, DomesticLeague, DomesticSeason, FootballStadium, FootballManager, DomesticSeasonMatch

class FootballTeamAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['league__counry', 'league',]

class FootballPlayerAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['team_playing', 'playing_position']

class DomesticLeagueAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['counry',]

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

admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(FootballPlayer, FootballPlayerAdmin)
admin.site.register(DomesticLeague, DomesticLeagueAdmin)
admin.site.register(DomesticSeason, DomesticSeasonAdmin)
admin.site.register(FootballStadium, FootballStadiumAdmin)
admin.site.register(FootballManager, FootballManagerAdmin)
admin.site.register(DomesticSeasonMatch, DomesticSeasonMatchAdmin)