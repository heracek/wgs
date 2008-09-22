from wgs.apps.graphs.forms import query_form_factory, QueryForm
from wgs.apps.graphs.models import Graph
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

import pprint

def graph_details(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id)
    
    return render_to_response('graphs/graph_details.html',
        { 'graph': graph },
        context_instance=RequestContext(request))

def graph_query(request):
    query_form_clean_pformat = ''
    
    if request.method == 'GET' and 'search' in request.GET:
        FactoredQueryForm = query_form_factory(request.GET)
        query_form = FactoredQueryForm(request.GET)
        if query_form.is_valid():
            query_form_clean_pformat = pprint.pformat(query_form.clean())
    else:
        query_form = QueryForm()
    return render_to_response('graphs/query.html', {
            'query_form': query_form,
            'query_form_clean_pformat': query_form_clean_pformat },
        context_instance=RequestContext(request))

def get_form_field_html(request, form_field_name):
    pass