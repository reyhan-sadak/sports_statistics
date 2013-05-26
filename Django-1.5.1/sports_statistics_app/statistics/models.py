from django.db import models

# Create your models here.

PLAYING_POSITIONS = {
    ('GK','Goalkeeper'),
    ('DF','Defender'),
    ('MF','Midfielder'),
    ('FW','Forward'),
}

class DomesticLeague(models.Model):
    # The name of the league (e.g. Premier League)
    name = models.CharField(max_length = 255)
    # The date the league was founded
    date_founded = models.DateField('date founded')
    # The country of the league
    counry = models.CharField(max_length = 255)
    # The most powerfull league has tier 0
    tier = models.PositiveIntegerField()
    def __str__(self):
        return self.name + ' , ' + self.counry
    
    class Meta:
        unique_together = (('name', 'counry'),)

class FootballStadium(models.Model):
    # The name of the stadium
    name = models.CharField(max_length = 255)
    # Location
    location = models.CharField(max_length = 255)
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = (('name', 'location'),)
        
class FootballManager(models.Model):
    # The name of the manager
    name = models.CharField(max_length = 255)
    # Place of birth
    place_of_birth = models.CharField(max_length = 255)
    # Birth day
    birth_day = models.DateField()
    def __str__(self):
        return self.name

class FootballTeam(models.Model):
    # The name of the team
    name = models.CharField(max_length = 255)
    # The date when the team was founded
    date_founded = models.DateField('date founded')
    # The league where the team currently plays
    league = models.ForeignKey(DomesticLeague)
    # Home stadium
    stadium = models.ForeignKey(FootballStadium)
    # Manager
    manager = models.ForeignKey(FootballManager)
    # Team logo
    #team_logo = models.FilePathField(null = True, path = 'D:\Python\Django-1.5.1\sports_statistics_app\statistics\resources')
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = (('name', 'league'),)

class FootballPlayer(models.Model):
    # The name of the player
    name = models.CharField(max_length = 255)
    # Date of birth
    birth_day = models.DateField()
    # Place of birth
    birth_place = models.CharField(max_length = 255)
    # Playing position
    playing_position = models.CharField(max_length = 2, choices = PLAYING_POSITIONS)
    # Kit Number
    kit_number = models.PositiveIntegerField()
    # Team Playing
    team_playing = models.ForeignKey(FootballTeam)
    # Player picture
    #player_picture = models.FilePathField(path = 'D:\Python\Django-1.5.1\sports_statistics_app\statistics\resources')
    def __str__(self):
        return self.name

class DomesticSeason(models.Model):
    # The league for which the season is
    league = models.ForeignKey(DomesticLeague)
    # The year in which the season finishes(e.g. the season 20012/2013 will have year 2013)
    year = models.PositiveIntegerField(null = False)
    # The number of the teams playing in the league this season
    number_of_teams = models.PositiveIntegerField(default = 0)
    # The number of teams which qualify directly for the first tournament
    num_direct_first_tournament = models.PositiveIntegerField(default = 0)
    # The number of teams which will play playoff for the first tournament
    num_playoff_first_tournament = models.PositiveIntegerField(default = 0)
    # The number of teams which qualify directly for the second tournament
    num_qualify_second_tournament = models.PositiveIntegerField(default = 0)
    # The number of teams which will play playoff for the second tournament
    num_playoff_second_tournament = models.PositiveIntegerField(default = 0)
    # The number of teams which will play plaoff for staying in the league
    num_playoff_relegation = models.PositiveIntegerField(default = 0)
    # The number of teams which will be relegated
    num_direct_relegation = models.PositiveIntegerField(default = 0)
    def __str__(self):
        name =  str(self.league) + ' ' + str(self.year - 1) + "/" + str(self.year)
        return name
    
    class Meta:
        unique_together = (('league', 'year'),)

class DomesticSeasonMatch(models.Model):
    # The season for which the match is
    season = models.ForeignKey(DomesticSeason)
    # Home team
    homeTeam = models.ForeignKey(FootballTeam, related_name = 'home_team')
    # Away team
    awayTeam = models.ForeignKey(FootballTeam, related_name = 'away_team')
    # Week
    week = models.PositiveIntegerField()
    # Time of the match
    time = models.DateTimeField()
    # Home team goals
    homeGoals = models.PositiveIntegerField(default = 0)
    # Away team goals
    awayGoals = models.PositiveIntegerField(default = 0)
    # Is match finished
    isFinished = models.BooleanField(default = False)
    def __str__(self):
        name = str(self.homeTeam) + ' - ' + str(self.awayTeam) + ' , ' + str(self.season) +' , week ' + str(self.week)
        return name