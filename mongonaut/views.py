from django.views.generic import DetailView
from django.views.generic import ListView

class AppListView(ListView):
    """ :args: <app_name> """
    pass

class DocumentListView(ListView):
    """ :args: <app_name> <document_name> """
    pass
    
class DocumentDetailView(DetailView):
    """ :args: <app_name> <document_name> <id> """
    pass

class DocumentEmbeddedDetailView(DetailView):
    """ :args: <app_name> <document_name> <id> <???> """
    pass