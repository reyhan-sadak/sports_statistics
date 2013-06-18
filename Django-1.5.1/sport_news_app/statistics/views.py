# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.utils.timezone import now
from SportNewsApp.navigationBar import getNavigationBar
from SportNewsApp.sideBar import getSideBar

from statistics.models import Country, DomesticLeague, FootballStadium, FootballTeam, DomesticSeason, DomesticSeasonMatch

POINTS_FOR_WIN = 3
POINTS_FOR_DRAW = 1
POINTS_FOR_LOST = 0

LAST_MATCHES_COUNT = 5

def statistics(request):
    supported_countries = {}
    for country in Country.objects.all():
        leagues = {}
        for league in DomesticLeague.objects.filter(country=country).order_by('tier'):
            leagues[league.id] = league.name
        supported_countries[country.id] = []
        supported_countries[country.id].append(country.name)
        supported_countries[country.id].append(leagues)
    if not supported_countries:
        raise Http404
    return render(request, 'statistics/statistics.html', {'navigationBar': getNavigationBar(),'side_bar': getSideBar(), 'supported_countries': supported_countries,})

def league(request, league_id):
    date = now()
    leagueYear = date.year
    season = int(request.GET.get('season', '-1'))
    if season != -1:
        leagueYear = season
    if date.month > 6:
        leagueYear += 1
    league = DomesticLeague.objects.filter(id=league_id)[0]
    teams = FootballTeam.objects.filter(league=league)
    season_query = DomesticSeason.objects.filter(league=league).filter(year=leagueYear)
    season = DomesticSeason
    if season_query:
        season = season_query[0]
    leagueMatches = DomesticSeasonMatch.objects.filter(season=season).filter(isFinished=True).order_by('-time')
    teamsInfo = []
    for team in teams:
        points = 0
        playedMatches = 0
        wins = 0
        draws = 0
        lost = 0
        goalsFor = 0
        goalsAgainst = 0
        last_matches = []
        for match in leagueMatches:
            if match.homeTeam == team:
                lastMatch = {}
                lastMatch['id'] = match.id
                goalsFor += match.homeGoals
                goalsAgainst += match.awayGoals
                playedMatches += 1
                if match.homeGoals > match.awayGoals:
                    wins += 1
                    lastMatch['result'] = 'win'
                elif match.homeGoals == match.awayGoals:
                    draws += 1
                    lastMatch['result'] = 'draw'
                else:
                    lost += 1
                    lastMatch['result'] = 'lost'
                if(len(last_matches) < LAST_MATCHES_COUNT):
                    last_matches.append(lastMatch)
            elif match.awayTeam == team:
                lastMatch = {}
                lastMatch['id'] = match.id
                goalsAgainst += match.homeGoals
                goalsFor += match.awayGoals
                playedMatches += 1
                if match.homeGoals < match.awayGoals:
                    wins += 1
                    lastMatch['result'] = 'win'
                elif match.homeGoals == match.awayGoals:
                    draws += 1
                    lastMatch['result'] = 'draw'
                else:
                    lost += 1
                    lastMatch['result'] = 'lost'
                if(len(last_matches) < LAST_MATCHES_COUNT):
                    last_matches.append(lastMatch)
        points = wins * POINTS_FOR_WIN + draws * POINTS_FOR_DRAW + lost * POINTS_FOR_LOST
        teamInfo = {}
        teamInfo['name'] = team.name
        teamInfo['points'] = points
        teamInfo['playedMatches'] = playedMatches
        teamInfo['wins'] = wins
        teamInfo['draws'] = draws
        teamInfo['lost'] = lost
        teamInfo['goalsFor'] = goalsFor
        teamInfo['goalsAgainst'] = goalsAgainst
        teamInfo['goalDiff'] = goalsFor - goalsAgainst
        teamInfo['lastMatches'] = last_matches
        teamInfo['id'] = team.id
        teamsInfo.append(teamInfo)
    sortedTeamsInfo = sorted(teamsInfo, key=lambda k: k['points'], reverse=True) 
    return render(request, 'statistics/league.html', {'season': season, 'teamsInfo': sortedTeamsInfo,})

def ranking(request, season_id):
    return HttpResponse("You are seeing the ranking of season:{}".format(season_id))

def stadiums(request):
    stadiums_list = FootballStadium.objects.order_by('name')
    #output = ','.join([p.name for p in stadiums_list])
    template = loader.get_template('statistics/stadiums.html')
    context = Context({
        'stadiums_list': stadiums_list,
    })
    return HttpResponse(template.render(context))

def stadium_info(request, stadium_id):
    try:
        stadium = FootballStadium.objects.get(pk=stadium_id)
    except FootballStadium.DoesNotExist:
        raise Http404
    return render(request, 'statistics/stadium_info.html', {'stadiumName': stadium.name})

#def ranking(request):
#    return HttpResponse("Ranking")