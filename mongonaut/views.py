from django.views.generic import DetailView
from django.views.generic import ListView

from mongonaut.sites import NautSite

class IndexView(ListView):
    queryset = NautSite._registry.iteritems()
    template_name = "mongonaut/index.html"

class AppListView(ListView):
    """ :args: <app_label> """

    template_name = "mongonaut/app_list.html"

class DocumentListView(ListView):
    """ :args: <app_label> <document_name> """
    template_name = "mongonaut/document_list.html"
    
class DocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> """
    template_name = "mongonaut/document_detail.html"

class EmbeddedDocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"