from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail
from wgs.apps.graphs.models import Graph
from wgs.apps.graphs.views import graph_details, graph_query

urlpatterns = patterns('',
    url(r'^query/$', graph_query, name='graph-query'),
    url(r'^graph/(?P<object_id>[1-9]\d*)/$', object_detail, { 'queryset': Graph.objects.all() }, name='graph-details'),
)
