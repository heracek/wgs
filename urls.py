from django.conf.urls.defaults import *
import os
import sys


urlpatterns = patterns('',
    # Example:
    # (r'^wgs/', include('wgs.foo.urls')),

    # Uncomment this for admin:
    url(r'^admin/', include('django.contrib.admin.urls')),
    url(r'', include('wgs.apps.graphs.urls')),
    url(r'^site-media/(.*)$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), 'site-media'))}),
)
