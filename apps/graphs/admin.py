from django.contrib import admin
import models

class GraphAdmin(admin.ModelAdmin):
    list_display = list_display_links = ['name', 'graph_matrix', 'order', 'size', 'connected', 'num_components', 'min_degree', 'max_degree', 'complete', 'regular', 'tree']
    search_fields = ['name', 'graph_matrix', 'order', 'size', 'connected', 'num_components', 'min_degree', 'max_degree', 'complete', 'regular', 'tree']
admin.site.register(models.Graph, GraphAdmin)
