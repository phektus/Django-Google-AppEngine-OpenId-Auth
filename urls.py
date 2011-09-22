from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    (r'^accounts/', include('django_gapps_openid.urls')),
    ('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
)
