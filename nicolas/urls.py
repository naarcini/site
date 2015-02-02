from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('nicolas.views',
    url(r'^$', 'comingsoon', name='comingsoon'),
    # url(r'^$', 'index', name='index'),
    # url(r'^resume/', 'resume', name='resume'),
    # url(r'^links/', 'links', name='links'),
    # url(r'^contact/', 'contact', name='contact'),
    # url(r'^nicolas/', include('nicolas.foo.urls')),

    # Indoor Robotic Navigation System URLs
    url(r'^webapp/', 'webapp', name='webapp'),
    url(r'^robot/', 'robot', name='robot'),
    url(r'^userInterface/', 'userInterface', name='userInterface'),
    url(r'^visualMap/', 'visualMap', name='visualMap'),
    url(r'^visualMapImages/', 'visualMapImages', name='visualMapImages'),
    url(r'^masterReset/', 'masterReset', name='masterReset'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
