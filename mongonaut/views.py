# -*- coding: utf-8 -*-
"""
    TODO move permission checks to the dispatch view thingee
"""

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.views.generic.edit import DeletionMixin
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from mongoengine.fields import EmbeddedDocumentField, ListField
from mongonaut.forms import DocumentListForm
from mongonaut.forms import DocumentDetailForm
from mongonaut.forms import document_detail_form_factory
from mongonaut.mixins import MongonautFormViewMixin
from mongonaut.mixins import MongonautViewMixin
from mongonaut.utils import is_valid_object_id


def setattr_doc(document, attr, value):
    """Used to set the value of a document.  Ensures an empty value may be given."""
    if value or isinstance(value, bool):
        setattr(document, attr, value)
    else:
        setattr(document, attr, None)


class IndexView(MongonautViewMixin, ListView):

    template_name = "mongonaut/index.html"
    queryset = []

    def get_queryset(self):
        return self.get_mongoadmins()


class AppListView(MongonautViewMixin, ListView):
    """ :args: <app_label> """

    template_name = "mongonaut/app_list.html"


class DocumentListView(MongonautViewMixin, FormView):
    """ :args: <app_label> <document_name>

        TODO - Make a generic document fetcher method
    """
    form_class = DocumentListForm
    success_url = '/'
    template_name = "mongonaut/document_list.html"
    permission = 'has_view_permission'

    documents_per_page = 25

    #def dispatch(self, *args, **kwargs):
    #    self.set_mongoadmin()
    #    self.set_permissions()
    #    return super(DocumentListView, self).dispatch(*args, **kwargs)

    def get_qset(self, queryset, q):
        if self.mongoadmin.search_fields and q:
            params = {}
            for field in self.mongoadmin.search_fields:
                if field == 'id':
                    # check to make sure this is a valid ID, otherwise we just continue
                    if is_valid_object_id(q):
                        return queryset.filter(id=q)
                    continue
                search_key = "{field}__icontains".format(field=field)
                params[search_key] = q

            queryset = queryset.filter(**params)
        return queryset

    def get_queryset(self):
        if hasattr(self, "queryset") and self.queryset:
            return self.queryset

        self.set_mongonaut_base()
        self.set_mongoadmin()
        self.document = getattr(self.models, self.document_name)
        queryset = self.document.objects.all()

        # search. move this to get_queryset
        # search. move this to get_queryset
        q = self.request.GET.get('q')
        self.get_qset(queryset, q)

        ### Start pagination
        ### Note:
        ###    Didn't use the Paginator in Django cause mongoengine querysets are
        ###    not the same as Django ORM querysets and it broke.
        # Make sure page request is an int. If not, deliver first page.
        try:
            self.page = int(self.request.GET.get('page', '1'))
        except ValueError:
            self.page = 1

        obj_count = queryset.count()
        self.total_pages = obj_count / self.documents_per_page + (1 if obj_count % self.documents_per_page else 0)

        if self.page < 1:
            self.page = 1

        if self.page > self.total_pages:
            self.page = self.total_pages

        start = (self.page - 1) * self.documents_per_page
        end = self.page * self.documents_per_page

        queryset = queryset[start:end] if obj_count else queryset

        self.queryset = queryset
        return queryset

    def get_initial(self):
        self.query = self.get_queryset()
        mongo_ids = {'mongo_id': [unicode(x.id) for x in self.query]}
        return mongo_ids

    def get_context_data(self, **kwargs):
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context = self.set_permissions_in_context(context)

        if not context['has_view_permission']:
            return HttpResponseForbidden("You do not have permissions to view this content.")

        context['object_list'] = self.get_queryset()

        context['document'] = self.document
        context['app_label'] = self.app_label
        context['document_name'] = self.document_name

        # pagination bits
        context['page'] = self.page
        context['documents_per_page'] = self.documents_per_page

        if self.page > 1:
            previous_page_number = self.page - 1
        else:
            previous_page_number = None

        if self.page < self.total_pages:
            next_page_number = self.page + 1
        else:
            next_page_number = None

        context['previous_page_number'] = previous_page_number
        context['has_previous_page'] = previous_page_number is not None
        context['next_page_number'] = next_page_number
        context['has_next_page'] = next_page_number is not None
        context['total_pages'] = self.total_pages

        # Part of upcoming list view form functionality
        if self.queryset.count():
            context['keys'] = ['id', ]

            # Show those items for which we've got list_fields on the mongoadmin
            for key in [x for x in self.document._fields.keys() if x != 'id' and x in self.mongoadmin.list_fields]:

                # TODO - Figure out why this EmbeddedDocumentField and ListField breaks this view
                # Note - This is the challenge part, right? :)
                if isinstance(self.document._fields[key], EmbeddedDocumentField):
                    continue
                if isinstance(self.document._fields[key], ListField):
                    continue
                context['keys'].append(key)

        if self.mongoadmin.search_fields:
            context['search_field'] = True

        return context

    def post(self, request, *args, **kwargs):
        # TODO - make sure to check the rights of the poster
        #self.get_queryset() # TODO - write something that grabs the document class better
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        mongo_ids = self.get_initial()['mongo_id']
        for form_mongo_id in form.data.getlist('mongo_id'):
            for mongo_id in mongo_ids:
                if form_mongo_id == mongo_id:
                    self.document.objects.get(id=mongo_id).delete()

        return self.form_invalid(form)


class DocumentDetailView(MongonautViewMixin, TemplateView):
    """ :args: <app_label> <document_name> <id> """
    template_name = "mongonaut/document_detail.html"
    permission = 'has_view_permission'

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        self.set_mongoadmin()
        context = self.set_permissions_in_context(context)
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)

        context['document'] = self.document
        context['app_label'] = self.app_label
        context['document_name'] = self.document_name
        context['keys'] = ['id', ]
        context['embedded_documents'] = []
        context['list_fields'] = []
        for key in sorted([x for x in self.document._fields.keys() if x != 'id']):
            # TODO - Figure out why this EmbeddedDocumentField and ListField breaks this view
            # Note - This is the challenge part, right? :)
            if isinstance(self.document._fields[key], EmbeddedDocumentField):
                context['embedded_documents'].append(key)
                continue
            if isinstance(self.document._fields[key], ListField):
                context['list_fields'].append(key)
                continue
            context['keys'].append(key)
        return context


class DocumentEditFormView(MongonautViewMixin, FormView, MongonautFormViewMixin):
    """ :args: <app_label> <document_name> <id> """

    template_name = "mongonaut/document_edit_form.html"
    form_class = DocumentDetailForm
    success_url = '/'
    permission = 'has_edit_permission'

    def get_success_url(self):
        self.set_mongonaut_base()
        return reverse('document_detail_edit_form', kwargs={'app_label': self.app_label, 'document_name': self.document_name, 'id': self.kwargs.get('id')})

    def get_context_data(self, **kwargs):
        context = super(DocumentEditFormView, self).get_context_data(**kwargs)
        self.set_mongoadmin()
        context = self.set_permissions_in_context(context)
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)

        context['document'] = self.document
        context['app_label'] = self.app_label
        context['document_name'] = self.document_name

        return context

    def get_form(self, DocumentDetailForm):
        self.set_mongoadmin()
        context = self.set_permissions_in_context({})

        if not context['has_edit_permission']:
            return HttpResponseForbidden("You do not have permissions to edit this content.")

        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)
        self.form = DocumentDetailForm()

        if self.request.method == 'POST':
            self.form = self.process_post_form('Your changes have been saved.')
        else:
            self.form = document_detail_form_factory(form=self.form, document_type=self.document_type, initial=self.document)
        return self.form


class DocumentAddFormView(MongonautViewMixin, FormView, MongonautFormViewMixin):
    """ :args: <app_label> <document_name> <id> """

    template_name = "mongonaut/document_add_form.html"
    form_class = DocumentDetailForm
    success_url = '/'
    permission = 'has_add_permission'

    def get_success_url(self):
        self.set_mongonaut_base()
        return reverse('document_detail', kwargs={'app_label': self.app_label, 'document_name': self.document_name, 'id': str(self.document.id)})

    def get_context_data(self, **kwargs):
        """ TODO - possibly inherit this from DocumentEditFormView. This is same thing minus:
            self.ident = self.kwargs.get('id')
            self.document = self.document_type.objects.get(id=self.ident)
        """
        context = super(DocumentAddFormView, self).get_context_data(**kwargs)
        self.set_mongoadmin()
        context = self.set_permissions_in_context(context)
        self.document_type = getattr(self.models, self.document_name)

        context['app_label'] = self.app_label
        context['document_name'] = self.document_name
        return context

    def get_form(self, DocumentDetailForm):
        self.set_mongonaut_base()
        self.document_type = getattr(self.models, self.document_name)
        self.form = DocumentDetailForm()

        if self.request.method == 'POST':
            self.form = self.process_post_form('Your new document has been added and saved.')
        else:
            self.form = document_detail_form_factory(form=self.form, document_type=self.document_type)
        return self.form


class DocumentDeleteView(DeletionMixin, MongonautViewMixin, TemplateView):
    """ :args: <app_label> <document_name> <id>

        TODO - implement a GET view for confirmation
    """

    success_url = "/"
    template_name = "mongonaut/document_delete.html"

    def get_success_url(self):
        self.set_mongonaut_base()
        messages.add_message(self.request, messages.INFO, 'Your document has been deleted.')
        return reverse('document_list', kwargs={'app_label': self.app_label, 'document_name': self.document_name})

    def get_object(self):
        self.set_mongoadmin()
        self.document_type = getattr(self.models, self.document_name)
        self.ident = self.kwargs.get('id')
        self.document = self.document_type.objects.get(id=self.ident)
        return self.document


class ListFieldListView(MongonautViewMixin, FormView):
    pass


class EmbeddedDocumentView(MongonautViewMixin, DetailView):
    pass


class EmbeddedDocumentDetailView(MongonautViewMixin, DetailView):
    """ :args: <app_label> <document_name> <id> <???> """
    template_name = "mongonaut/embedded_document_detail.html"
