from django.conf.urls import patterns, include, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^categories/(?P<category_id>\d+)/$', views.category, name='category_id'),
    url(r'^categories/(\d+)/(\d+)/$', views.sub_category),
    url(r'^(?P<news_id>\d+)/$', views.news, name='news_id'),
)