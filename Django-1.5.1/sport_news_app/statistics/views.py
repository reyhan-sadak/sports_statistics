# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.utils.timezone import now
from SportNewsApp.navigationBar import getNavigationBar

from statistics.models import Country, DomesticLeague, FootballStadium, FootballTeam, DomesticSeason, DomesticSeasonMatch

POINTS_FOR_WIN = 3
POINTS_FOR_DRAW = 1
POINTS_FOR_LOST = 0

LAST_MATCHES_COUNT = 5

def getLeagueYear():
    date = now()
    leagueYear = date.year
    if date.month >= 6:
        leagueYear += 1
    return leagueYear

def getStatisticsSideBar(league_id=1):
    supported_countries = {}
    for country in Country.objects.all():
        leagues = {}
        shouldIncludeLeagues = False
        for league in DomesticLeague.objects.filter(country=country).order_by('tier'):
            leagues[league.id] = league.name
            if int(league_id) == league.id:
                shouldIncludeLeagues = True
        supported_countries[country.id] = []
        supported_countries[country.id].append(country.name)
        if shouldIncludeLeagues:
            supported_countries[country.id].append(leagues)
    return supported_countries

def getLeagueRanking(leagueYear, league_id=1):
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
        teamInfo['team_logo'] = team.team_logo
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
    sortedTeamsInfo = sorted(teamsInfo, key=lambda k: k['name'])
    twiceSortedTeamsInfo = sorted(sortedTeamsInfo, key=lambda k: k['goalDiff'], reverse=True)
    tripleSortedTeamsInfo = sorted(twiceSortedTeamsInfo, key=lambda k: k['points'], reverse=True)
    return tripleSortedTeamsInfo

def statistics(request):
    return league(request, 1)

def country(request, country_id):
    league_id = 1
    leagues = DomesticLeague.objects.filter(country__id=country_id).order_by('tier')
    if leagues:
        league_id = leagues[0].id
    return league(request, league_id)

def league(request, league_id):
    return render(request, 'statistics/league.html', {'navigationBar': getNavigationBar(),'side_bar': getStatisticsSideBar(league_id), 'teamsInfo': getLeagueRanking(getLeagueYear(), league_id),})

def teamInfo(request, team_id):
    league_id = 1
    team = FootballTeam.objects.filter(id=team_id)
    if team:
        teamInfo = team[0]
    else:
        raise Http404
    teamInfoToShow = {}
    teamInfoToShow['name'] = teamInfo.name
    teamInfoToShow['info'] = teamInfo.info
    teamInfoToShow['date_founded'] = teamInfo.date_founded
    teamInfoToShow['league'] = teamInfo.league
    teamInfoToShow['stadium'] = teamInfo.stadium
    teamInfoToShow['manager'] = teamInfo.manager
    teamInfoToShow['team_logo'] = teamInfo.team_logo
    league_id = teamInfo.league.id
    season_query = DomesticSeason.objects.filter(league=teamInfo.league).filter(year=getLeagueYear())
    season = DomesticSeason
    if season_query:
        season = season_query[0]
    matchesFromTheSeason = DomesticSeasonMatch.objects.filter(season=season).order_by('week')
    passedMatches = []
    upComingMatches = []
    for match in matchesFromTheSeason:
        if match.homeTeam == teamInfo or match.awayTeam == teamInfo:
            if match.isFinished:
                passedMatches.append(match)
            else:
                upComingMatches.append(match)
    teamInfoToShow['passedMatches'] = passedMatches[:5]
    teamInfoToShow['upComingMatches'] = upComingMatches[:5]
    return render(request, 'statistics/teamInfo.html', {'navigationBar': getNavigationBar(), 'side_bar': getStatisticsSideBar(league_id), 'teamInfoToShow': teamInfoToShow})

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

def manager_info(request, manager_id):
    return HttpResponse("Manager info about manager with id = " + manager_id)

#def ranking(request):
#    return HttpResponse("Ranking")