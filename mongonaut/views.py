from django.views.generic import DetailView
from django.views.generic import ListView

from mongonaut.sites import NautSite

class IndexView(ListView):
    queryset = NautSite._registry.iteritems()
    template_name = "mongonaut/index.html"

class AppListView(ListView):
    """ :args: <app_label> """
    pass

class DocumentListView(ListView):
    """ :args: <app_label> <document_name> """
    pass
    
class DocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> """
    pass

class DocumentEmbeddedDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> <???> """
    pass