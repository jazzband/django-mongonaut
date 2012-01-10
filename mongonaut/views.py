from django.utils.importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from mongoengine.fields import EmbeddedDocumentField, ListField

from mongonaut.forms import DocumentListForm

class AppStore(object):
    
    def __init__(self, module):
        self.models = []
        for key in module.__dict__.keys():
            model_candidate = getattr(module, key)
            if hasattr(model_candidate, 'mongoadmin'):
                self.add_model(model_candidate)
                
    def add_model(self, model):
        model.name = model.__name__
        self.models.append(model)
        

class IndexView(ListView):

    template_name = "mongonaut/index.html"
    queryset = []
    
    def get_queryset(self):
        apps = []
        for app_name in settings.INSTALLED_APPS:
            mongoadmin = "{0}.mongoadmin".format(app_name)
            try:
                module = import_module(mongoadmin)
            except ImportError:
                print app_name
                continue
            
            app_store = AppStore(module)
            apps.append(dict(
                app_name=app_name,
                obj=app_store
            ))
        return apps

class AppListView(ListView):
    """ :args: <app_label> """

    template_name = "mongonaut/app_list.html"

class DocumentListView(FormView):
    """ :args: <app_label> <document_name> 
    
        TODO - Make a generic document fetcher method
    """
    form_class = DocumentListForm
    success_url = '/'
    template_name = "mongonaut/document_list.html"
    
    def get_queryset(self):
        self.app_label = self.kwargs.get('app_label')
        self.document_name = self.kwargs.get('document_name')
        
        # TODO Allow this to be assigned via url variable
        models_name = self.kwargs.get('models_name', 'models')
        
        # import the models file
        model_name = "{0}.{1}".format(self.app_label, models_name)
        models = import_module(model_name)
        
        # now get the document
        self.document = getattr(models, self.document_name)
        self.queryset = self.document.objects.all()
        return self.queryset
        
    def get_initial(self):
        mongo_ids = {'mongo_id':[unicode(x.id) for x in self.get_queryset()]}
        return mongo_ids
        
    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        
        context['object_list'] = self.get_queryset()        
        context['document'] = self.document
        context['app_label'] = self.app_label  
        context['document_name'] = self.document_name

        if self.queryset.count():
            context['keys'] = ['id',]
            for key in sorted([x for x in self.document._fields.keys() if x != 'id']):
                # TODO - Figure out why this EmbeddedDocumentField and ListField breaks this view
                # Note - This is the challenge part, right? :)
                if isinstance(self.document._fields[key], EmbeddedDocumentField):            
                    continue
                if isinstance(self.document._fields[key], ListField):                                
                    continue
                context['keys'].append(key)
        return context                
                
    def post(self, request, *args, **kwargs):
        # TODO - make sure to check the rights of the poster
        self.get_queryset() # TODO - write something that grabs the document class better
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        mongo_ids = self.get_initial()['mongo_id']             
        for form_mongo_id in form.data.getlist('mongo_id'):
            for mongo_id in mongo_ids:
                if form_mongo_id == mongo_id:
                    self.document.objects.get(id=mongo_id).delete()
            
        return self.form_invalid(form)                                    


    
class DocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> """
    template_name = "mongonaut/document_detail.html"

class EmbeddedDocumentDetailView(DetailView):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"