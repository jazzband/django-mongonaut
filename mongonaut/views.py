import importlib

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
    queryset = []

    def get_queryset(self):
        app_label = self.kwargs.get('app_label')
        document_name = self.kwargs.get('document_name')

        # TODO Allow this to be assigned via url variable
        models_name = self.kwargs.get('models_name', 'models')

        # import the models file
        model_name = "{0}.{1}".format(app_label, models_name)
        models = importlib.import_module(model_name)

        # now get the document
        self.document = getattr(models, document_name)
        self.queryset = self.document.objects.all()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context['document_name'] = self.kwargs.get('document_name')
        context['document'] = self.document

        if self.queryset.count():
            context['keys'] = sorted(self.document._fields.keys())

        return context

    
class DocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> """
    template_name = "mongonaut/document_detail.html"

class EmbeddedDocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"