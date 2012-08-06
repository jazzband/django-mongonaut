# -*- coding: utf-8 -*-

import ast
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.forms import widgets
from django.forms.widgets import DateTimeInput, CheckboxInput
from django.http import HttpResponseForbidden
from django.utils.importlib import import_module

from mongonaut.exceptions import NoMongoAdminSpecified
from mongonaut.forms import document_detail_form_factory
from mongonaut.widgets import ListFieldWidget


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


class MongonautViewMixin(object):

    def render_to_response(self, context, **response_kwargs):
        if hasattr(self, 'permission') and self.permission not in context:
            return HttpResponseForbidden("You do not have permissions to access this content.")

        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(MongonautViewMixin, self).get_context_data(**kwargs)
        context['MONGONAUT_JQUERY'] = getattr(settings, "MONGONAUT_JQUERY", "http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js")
        context['MONGONAUT_TWITTER_BOOTSTRAP'] = getattr(settings, "MONGONAUT_TWITTER_BOOTSTRAP", "http://twitter.github.com/bootstrap/assets/css/bootstrap.css")
        context['MONGONAUT_TWITTER_BOOTSTRAP_ALERT'] = getattr(settings, "MONGONAUT_TWITTER_BOOTSTRAP_ALERT", "http://twitter.github.com/bootstrap/assets/js/bootstrap-alert.js")
        return context

    def get_mongoadmins(self):
        """ Returns a list of all mongoadmin implementations for the site """
        apps = []
        for app_name in settings.INSTALLED_APPS:
            mongoadmin = "{0}.mongoadmin".format(app_name)
            try:
                module = import_module(mongoadmin)
            except ImportError as e:
                if str(e) == "No module named mongoadmin":
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
    """View used to help with processing of posted forms for add and edit forms
    """

    def process_post_form(self, success_message=None):
        """As long as the form is set on the view this method will validate the for and
        save the submitted data.  Only call this if you are posting data.  The given success_message
        will be used with the djanog messages framework if the posted data sucessfully submits.
        """
        initial_arg = self.document if hasattr(self, 'document') else None
        self.form = document_detail_form_factory(form=self.form, document_type=self.document_type, initial=initial_arg,
                                                 post_data=self.request.POST)
        self.form.data = self.request.POST
        self.form.is_bound = True
        if self.form.is_valid():
            # When on initial args are given we need to set the base document.
            if initial_arg is None:
                self.document = self.document_type()
            # Need  keep track of each listfield submitted
            list_fields_dict = {}
            for key, field in self.form.fields.items():
                posted_value = self.request.POST.get(key, None)

                if 'readonly' in field.widget.attrs:
                    # For _id or things specified as such
                    continue

                if isinstance(field.widget, ListFieldWidget):
                    # Need to know what list this data belongs to
                    list_key = key.split('_')

                    # If the last value is not an integer we will raise a value error most likely
                    try:
                        if isinstance(ast.literal_eval(list_key[-1]), int):
                            del list_key[-1]
                    except ValueError:
                        pass
                    list_key = u"_".join(list_key)

                    # Get the value based on field type and append it to the existing list
                    if isinstance(field.widget, DateTimeInput):
                        format = field.widget.format
                        value = datetime.strptime(posted_value, format) if posted_value else None
                    elif isinstance(field.widget, widgets.Select):
                        # supporting reference fields!
                        value = field.mongofield.document_type.objects.get(id=posted_value) if posted_value else None
                    else:
                        value = self.form.cleaned_data[key]

                    if list_key in list_fields_dict:
                        list_fields_dict[list_key].append(value)
                    else:
                        list_fields_dict[list_key] = [value]
                    continue

                if isinstance(field.widget, CheckboxInput):
                    value = self.form.cleaned_data[key]
                    setattr(self.document, key, value)
                    continue

                if isinstance(field.widget, DateTimeInput):
                    format = field.widget.format
                    value = datetime.strptime(posted_value, format) if posted_value else None
                    setattr(self.document, key, value)
                    continue

                if isinstance(field.widget, widgets.Select):
                    # supporting reference fields!
                    value = field.mongofield.document_type.objects.get(id=posted_value) if posted_value else None
                    setattr(self.document, key, value)
                    continue

                # for strings
                setattr(self.document, key, self.form.cleaned_data[key])

            for key, list_values in list_fields_dict.iteritems():
                # Remove None items from the list so blank fields can be submitted
                list_values = filter(None, list_values)
                setattr(self.document, key, list_values)

            self.document.save()
            if success_message:
                messages.add_message(self.request, messages.INFO, success_message)
        return self.form
