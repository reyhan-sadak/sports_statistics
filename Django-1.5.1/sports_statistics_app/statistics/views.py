# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from statistics.models import FootballStadium

def index(request):
    return HttpResponse("Hello, world!")

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