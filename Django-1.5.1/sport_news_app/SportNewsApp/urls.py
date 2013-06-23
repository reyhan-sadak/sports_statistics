from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from main import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SportNewsApp.views.home', name='home'),
    # url(r'^SportNewsApp/', include('SportNewsApp.foo.urls')),
    
    url(r'^$', include('main.urls')),
    url(r'^news/', include('main.urls')),
    url(r'^accounts/', include('main.urls')),
    url(r'^info/', views.info, name='info'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^statistics/', include('statistics.urls')),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT } ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
    )