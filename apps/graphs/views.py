from wgs.apps.graphs.forms import QueryForm
from wgs.apps.graphs.models import Graph
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

def graph_details(request, graph_id):
    graph = get_object_or_404(Graph, pk=graph_id)
    
    return render_to_response('graphs/graph_details.html',
        { 'graph': graph },
        context_instance=RequestContext(request))

def graph_query(request):
    if request.method == 'GET' and 'search' in request.GET:
        query_form = QueryForm(request.GET)
        if query_form.is_valid():
            pass
            #print query_form.clean()
    else:
        query_form = QueryForm()
    #print query_form.as_p()
    return render_to_response('graphs/query.html',
        { 'query_form': query_form },
        context_instance=RequestContext(request))

def get_form_field_html(request, form_field_name):
    pass