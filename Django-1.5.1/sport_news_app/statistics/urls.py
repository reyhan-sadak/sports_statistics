from django.conf.urls import patterns, include, url
from statistics import views

urlpatterns = patterns('',
    url(r'^$', views.statistics, name='statistics'),
    url(r'^leagues/(\d+)/$', views.league, name='league'),
    url(r'^countries/(?P<country_id>\d+)/$', views.country, name='country'),
    url(r'^teams/(?P<team_id>\d+)/$', views.teamInfo, name='teamInfo'),
    url(r'^ranking/season/(?P<season_id>\d+)/$', views.ranking, name='ranking'),
    #url(r'^ranking', views.ranking, name='ranking'),
    url(r'^stadiums/(?P<stadium_id>\d+)/$', views.stadium_info, name='stadium_info'),
    #url(r'^stadiums', views.stadiums, name='stadiums'),
    url(r'^managers/(?P<manager_id>\d+)/$', views.manager_info, name='manager_info'),
)