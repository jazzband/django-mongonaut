from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from mongoengine.fields import EmbeddedDocumentField, ListField

from mongonaut.forms import DocumentListForm
from mongonaut.mixins import MongonautViewMixin

class IndexView(ListView, MongonautViewMixin):

    template_name = "mongonaut/index.html"
    queryset = []
    
    def get_queryset(self):
        return self.get_mongoadmins()

class AppListView(ListView, MongonautViewMixin):
    """ :args: <app_label> """

    template_name = "mongonaut/app_list.html"

class DocumentListView(FormView, MongonautViewMixin):
    """ :args: <app_label> <document_name> 
    
        TODO - Make a generic document fetcher method
    """
    form_class = DocumentListForm
    success_url = '/'
    template_name = "mongonaut/document_list.html"
    
    def get_queryset(self):
        self.set_mongonaut_base()
        self.document = getattr(self.models, self.document_name)
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

class DocumentDetailView(TemplateView, MongonautViewMixin):
    """ :args: <app_label> <document_name> <id> """
    template_name = "mongonaut/document_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        self.set_mongonaut_base()
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)
        
        context['document'] = self.document
        context['app_label'] = self.app_label  
        context['document_name'] = self.document_name
        context['keys'] = ['id',]
        for key in sorted([x for x in self.document._fields.keys() if x != 'id']):
            # TODO - Figure out why this EmbeddedDocumentField and ListField breaks this view
            # Note - This is the challenge part, right? :)
            if isinstance(self.document._fields[key], EmbeddedDocumentField):            
                continue
            if isinstance(self.document._fields[key], ListField):                                
                continue
            context['keys'].append(key)
            
        self.set_mongoadmin()
        context = self.get_permissions(context)

        return context
 
# TODO - get working
#class DocumentDetailFormView(FormView):
#    """ :args: <app_label> <document_name> <id> """#

#    template_name = "mongonaut/document_detail_form.html"
#    form_class = DocumentListForm
#    success_url = '/'

class EmbeddedDocumentDetailView(DetailView, MongonautViewMixin):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"