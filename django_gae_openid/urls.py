from django.conf.urls.defaults import *

urlpatterns = patterns('django_gapps_openid.views',
    url(r'^login/$', 'login_begin'),
    url(r'^logout/$', 'logout_view'),
    url(r'^complete/$', 'login_complete'),
)
