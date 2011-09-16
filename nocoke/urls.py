from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('nocoke.monitor.views',
    # Examples:
    url(r'^$', 'index', name='index'),
    url(r'^flow/?$', 'flow', name='flow'),
    # url(r'^nocoke/', include('nocoke.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
