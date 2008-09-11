from django.db import models

class Graph(models.Model):
    name = models.CharField(blank=True, max_length=100)
    graph_matrix = models.TextField()
    order = models.IntegerField()
    size = models.IntegerField()
    connected = models.NullBooleanField(blank=True, null=True)
    num_components = models.IntegerField(blank=True, null=True)
    min_degree = models.IntegerField(blank=True, null=True)
    max_degree = models.IntegerField(blank=True, null=True)
    complete = models.NullBooleanField(blank=True, null=True)
    regular = models.NullBooleanField(blank=True, null=True)
    tree = models.NullBooleanField(blank=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
