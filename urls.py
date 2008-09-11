from django.conf.urls.defaults import *
from django.contrib import admin
import os
import sys

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/(.*)', admin.site.root),
    url(r'', include('wgs.apps.graphs.urls')),
    url(r'^site-media/(.*)$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.join(os.path.dirname(__file__), 'site-media'))}),
)
