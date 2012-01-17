from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


from mongoengine.fields import EmbeddedDocumentField, ListField

from mongonaut.forms import DocumentListForm
from mongonaut.forms import DocumentDetailForm
from mongonaut.forms import document_detail_form_factory
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
        
        ### Start pagination
        ### Note: 
        ###    Didn't use the Paginator in Django cause mongoengine querysets are 
        ###    not the same as Django ORM querysets and it broke.
        # Make sure page request is an int. If not, deliver first page.
        try:
            page = int(self.request.GET.get('page', '1'))
        except ValueError:
            page = 1
        context['page'] = page
            
        documents_per_page = 25
        context['total_pages'] = max(context['object_list'].count() / documents_per_page, 1)
        start = (page -1) * documents_per_page
        end = page * documents_per_page
        context['previous_page_number'] = page - 1        
        context['next_page_number'] = page + 1
        try:
            context['object_list'] = context['object_list'][start:end]
        except Exception as e:
            print e
                
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
 

class DocumentDetailFormView(FormView, MongonautViewMixin):
    """ :args: <app_label> <document_name> <id> """#

    template_name = "mongonaut/document_detail_form.html"
    form_class = DocumentDetailForm
    success_url = '/'
    
    def get_success_url(self):
        self.set_mongonaut_base()  
        return reverse('document_detail_form', kwargs={'app_label':self.app_label,'document_name':self.document_name,'id':self.kwargs.get('id')})    
    
    def get_context_data(self, **kwargs):
        context = super(DocumentDetailFormView, self).get_context_data(**kwargs)
        self.set_mongonaut_base()
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)
        
        context['document'] = self.document
        context['app_label'] = self.app_label  
        context['document_name'] = self.document_name
            
        self.set_mongoadmin()
        context = self.get_permissions(context)
        #self.form = DocumentDetailForm()
        #context['form'] = document_detail_form_munger(self.form, self.document_type, self.document)
        
        #if self.request.method == 'POST':
        #    context['form'].data = self.request.POST
        #    context['form'].is_bound = True

        return context
        
    def get_form(self, DocumentDetailForm):
        self.set_mongonaut_base()
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)
        self.form = DocumentDetailForm()        
        self.form = document_detail_form_factory(self.form, self.document_type, self.document)
        if self.request.method == 'POST':
            self.form.data = self.request.POST
            self.form.is_bound = True
            if self.form.is_valid():
                for key, value in self.form.fields.items():
                    #if hasattr(value, 'document_type_obj') or hasattr(value, 'field'):
                    if 'readonly' in value.widget.attrs:
                        # For _id
                        # for ReferenceField - like <class 'articles.models.User'> on Blog                        
                        # For ListField - like 'field': <mongoengine.fields.StringField object at 0x101b51810>,                                
                        continue
                    setattr(self.document, key, self.request.POST[key])
                self.document.save()
                # TODO add message for save

            
        return self.form
        
    

class EmbeddedDocumentDetailView(DetailView, MongonautViewMixin):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"