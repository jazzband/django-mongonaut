# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseForbidden
from importlib import import_module
from mongoengine.fields import EmbeddedDocumentField

from mongonaut.exceptions import NoMongoAdminSpecified
from mongonaut.forms import MongoModelForm
from mongonaut.forms.form_utils import has_digit
from mongonaut.forms.form_utils import make_key
from mongonaut.utils import translate_value
from mongonaut.utils import trim_field_key


class AppStore(object):
    """Represents Django apps in the django-mongonaut admin."""

    def __init__(self, module):
        self.models = []
        for key in module.__dict__.keys():
            model_candidate = getattr(module, key)
            if hasattr(model_candidate, 'mongoadmin'):
                self.add_model(model_candidate)

    def add_model(self, model):
        model.name = model.__name__
        self.models.append(model)


class MongonautViewMixin(object):
    """Used for all views in the project, handles authorization to content,
        viewing, controlling and setting of data.
    """

    def render_to_response(self, context, **response_kwargs):
        if hasattr(self, 'permission') and not self.request.user.has_perm(self.permission):
            return HttpResponseForbidden("You do not have permissions to access this content.")

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(MongonautViewMixin, self).get_context_data(**kwargs)
        context['MONGONAUT_JQUERY'] = getattr(settings, "MONGONAUT_JQUERY",
                                      "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js")
        context['MONGONAUT_TWITTER_BOOTSTRAP'] = getattr(settings, "MONGONAUT_TWITTER_BOOTSTRAP",
                                                 "//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css")
        context['MONGONAUT_TWITTER_BOOTSTRAP_ALERT'] = getattr(settings,
                                                               "MONGONAUT_TWITTER_BOOTSTRAP_ALERT",
                                                       "//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js")
        return context

    def get_mongoadmins(self):
        """ Returns a list of all mongoadmin implementations for the site """
        apps = []
        for app_name in settings.INSTALLED_APPS:
            mongoadmin = "{0}.mongoadmin".format(app_name)
            try:
                module = import_module(mongoadmin)
            except ImportError as e:
                if str(e).startswith("No module named"):
                    continue
                raise e

            app_store = AppStore(module)
            apps.append(dict(
                app_name=app_name,
                obj=app_store
            ))
        return apps

    def set_mongonaut_base(self):
        """ Sets a number of commonly used attributes """
        if hasattr(self, "app_label"):
            # prevents us from calling this multiple times
            return None
        self.app_label = self.kwargs.get('app_label')
        self.document_name = self.kwargs.get('document_name')

        # TODO Allow this to be assigned via url variable
        self.models_name = self.kwargs.get('models_name', 'models')

        # import the models file
        self.model_name = "{0}.{1}".format(self.app_label, self.models_name)
        self.models = import_module(self.model_name)

    def set_mongoadmin(self):
        """ Returns the MongoAdmin object for an app_label/document_name style view
        """
        if hasattr(self, "mongoadmin"):
            return None

        if not hasattr(self, "document_name"):
            self.set_mongonaut_base()

        for mongoadmin in self.get_mongoadmins():
            for model in mongoadmin['obj'].models:
                if model.name == self.document_name:
                    self.mongoadmin = model.mongoadmin
                    break
        # TODO change this to use 'finally' or 'else' or something
        if not hasattr(self, "mongoadmin"):
            raise NoMongoAdminSpecified("No MongoAdmin for {0}.{1}".format(self.app_label, self.document_name))

    def set_permissions_in_context(self, context={}):
        """ Provides permissions for mongoadmin for use in the context"""

        context['has_view_permission'] = self.mongoadmin.has_view_permission(self.request)
        context['has_edit_permission'] = self.mongoadmin.has_edit_permission(self.request)
        context['has_add_permission'] = self.mongoadmin.has_add_permission(self.request)
        context['has_delete_permission'] = self.mongoadmin.has_delete_permission(self.request)
        return context


class MongonautFormViewMixin(object):
    """
    View used to help with processing of posted forms.
    Must define self.document_type for process_post_form to work.
    """

    def process_post_form(self, success_message=None):
        """
        As long as the form is set on the view this method will validate the form
        and save the submitted data.  Only call this if you are posting data.
        The given success_message will be used with the djanog messages framework
        if the posted data sucessfully submits.
        """

        # When on initial args are given we need to set the base document.
        if not hasattr(self, 'document') or self.document is None:
            self.document = self.document_type()
        self.form = MongoModelForm(model=self.document_type, instance=self.document,
                                   form_post_data=self.request.POST).get_form()
        self.form.is_bound = True
        if self.form.is_valid():

            self.document_map_dict = MongoModelForm(model=self.document_type).create_document_dictionary(self.document_type)
            self.new_document = self.document_type

            # Used to keep track of embedded documents in lists.  Keyed by the list and the number of the
            # document.
            self.embedded_list_docs = {}

            if self.new_document is None:
                messages.error(self.request, u"Failed to save document")
            else:
                self.new_document = self.new_document()

                for form_key in self.form.cleaned_data.keys():
                    if form_key == 'id' and hasattr(self, 'document'):
                        self.new_document.id = self.document.id
                        continue
                    self.process_document(self.new_document, form_key, None)

                self.new_document.save()
                if success_message:
                    messages.success(self.request, success_message)

        return self.form

    def process_document(self, document, form_key, passed_key):
        """
        Given the form_key will evaluate the document and set values correctly for
        the document given.
        """
        if passed_key is not None:
            current_key, remaining_key_array = trim_field_key(document, passed_key)
        else:
            current_key, remaining_key_array = trim_field_key(document, form_key)

        key_array_digit = remaining_key_array[-1] if remaining_key_array and has_digit(remaining_key_array) else None
        remaining_key = make_key(remaining_key_array)

        if current_key.lower() == 'id':
            raise KeyError(u"Mongonaut does not work with models which have fields beginning with id_")

        # Create boolean checks to make processing document easier
        is_embedded_doc = (isinstance(document._fields.get(current_key, None), EmbeddedDocumentField)
                          if hasattr(document, '_fields') else False)
        is_list = not key_array_digit is None
        key_in_fields = current_key in document._fields.keys() if hasattr(document, '_fields') else False

        # This ensures you only go through each documents keys once, and do not duplicate data
        if key_in_fields:
            if is_embedded_doc:
                self.set_embedded_doc(document, form_key, current_key, remaining_key)
            elif is_list:
                self.set_list_field(document, form_key, current_key, remaining_key, key_array_digit)
            else:
                value = translate_value(document._fields[current_key],
                                        self.form.cleaned_data[form_key])
                setattr(document, current_key, value)

    def set_embedded_doc(self, document, form_key, current_key, remaining_key):
        """Get the existing embedded document if it exists, else created it."""

        embedded_doc = getattr(document, current_key, False)
        if not embedded_doc:
            embedded_doc = document._fields[current_key].document_type_obj()

        new_key, new_remaining_key_array = trim_field_key(embedded_doc, remaining_key)
        self.process_document(embedded_doc, form_key, make_key(new_key, new_remaining_key_array))
        setattr(document, current_key, embedded_doc)

    def set_list_field(self, document, form_key, current_key, remaining_key, key_array_digit):
        """1. Figures out what value the list ought to have
           2. Sets the list
        """

        document_field = document._fields.get(current_key)

        # Figure out what value the list ought to have
        # None value for ListFields make mongoengine very un-happy
        list_value = translate_value(document_field.field, self.form.cleaned_data[form_key])
        if list_value is None or (not list_value and not bool(list_value)):
            return None

        current_list = getattr(document, current_key, None)

        if isinstance(document_field.field, EmbeddedDocumentField):
            embedded_list_key = u"{0}_{1}".format(current_key, key_array_digit)

            # Get the embedded document if it exists, else create it.
            embedded_list_document = self.embedded_list_docs.get(embedded_list_key, None)
            if embedded_list_document is None:
                embedded_list_document = document_field.field.document_type_obj()

            new_key, new_remaining_key_array = trim_field_key(embedded_list_document, remaining_key)
            self.process_document(embedded_list_document, form_key, new_key)

            list_value = embedded_list_document
            self.embedded_list_docs[embedded_list_key] = embedded_list_document

            if isinstance(current_list, list):
                # Do not add the same document twice
                if embedded_list_document not in current_list:
                    current_list.append(embedded_list_document)
            else:
                setattr(document, current_key, [embedded_list_document])

        elif isinstance(current_list, list):
            current_list.append(list_value)
        else:
            setattr(document, current_key, [list_value])
