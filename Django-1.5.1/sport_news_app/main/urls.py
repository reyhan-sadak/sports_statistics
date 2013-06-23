from django.conf.urls import patterns, include, url
from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login_view'),
    url(r'^logout/$', views.logout_view, name='logout_view'),
    url(r'^signup/$', views.create_account, name='create_account'),
    url(r'^categories/(?P<category_id>\d+)/$', views.category, name='category_id'),
    url(r'^categories/(\d+)/(\d+)/$', views.sub_category),
    url(r'^(?P<news_id>\d+)/$', views.news, name='news_id'),
    url(r'^searchNews/$', views.search_news, name='search'),
    url(r'^comment/$', views.comment_news, name='comment'),
)