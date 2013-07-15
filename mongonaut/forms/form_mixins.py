# -*- coding: utf-8 -*-

from copy import deepcopy

from django import forms
from mongoengine.base import BaseList
from mongoengine.base import TopLevelDocumentMetaclass
from mongoengine.fields import Document
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.fields import ListField
from mongoengine.fields import ReferenceField

from .form_utils import FieldTuple
from .form_utils import has_digit
from .form_utils import make_key
from .widgets import get_form_field_class
from mongonaut.utils import trim_field_key


CHECK_ATTRS = {'required': 'required',
               'help_text': 'help_text',
               'name': 'name'}


def get_document_unicode(document):
    try:
        return document.__unicode__()
    except AttributeError:
        return unicode(document)


class MongoModelFormBaseMixin(object):
    """
    For use with mongoengine.

    This mixin should not be used alone it should be used to inherit from.

    This mixin provides functionality for generating a form.  Provides 4 methods
    useful for putting data on a form:

    get_form_field_dict -- creates a keyed tuple representation of a model field used
                           to create form fields
    set_form_fields -- takes the form field dictionary and sets all values on a form
    set_form_field -- sets an individual form field
    get_field_value -- returns the value for the field

    If you inherit from this class you will need to call the above methods
    with the correct values, see forms.py for an example.
    """

    def __init__(self, model, instance=None, form_post_data=None):
        """
        Params:
            model          -- The model class to create the form with
            instance       -- An instance of the model class can be used to
                              initialize data.
            form_post_data -- Values given by request.POST
        """
        self.model = model
        self.model_instance = instance
        self.post_data_dict = form_post_data
        # Preferred for symantic checks of model_instance
        self.is_initialized = False if instance is None else True
        self.form = forms.Form()

        if not isinstance(self.model, TopLevelDocumentMetaclass):
            raise TypeError(u"The model supplied must be a mongoengine Document")

        if self.is_initialized and not isinstance(self.model_instance, self.model):
            raise TypeError(u"The provided instance must be an instance of the given model")

        if self.post_data_dict is not None and not isinstance(self.post_data_dict, dict):
            raise TypeError(u"You must pass in a dictionary for form_post_data")

    def get_form_field_dict(self, model_dict):
        """
        Takes a model dictionary representation and creates a dictionary
        keyed by form field.  Each value is a  keyed 4 tuple of:
        (widget, mode_field_instance, model_field_type, field_key)
        """
        return_dict = {}
        for field_key, field_dict in model_dict.iteritems():
            if not field_key.startswith("_"):
                widget = field_dict.get('_widget', None)
                if widget is None:
                    return_dict[field_key] = self.get_form_field_dict(field_dict)
                    return_dict[field_key].update({'_field_type': field_dict.get('_field_type', None)})
                else:
                    return_dict[field_key] = FieldTuple(widget,
                                             field_dict.get('_document_field', None),
                                             field_dict.get('_field_type', None),
                                             field_dict.get('_key', None))
        return return_dict

    def set_form_fields(self, form_field_dict, parent_key=None, field_type=None):
        """
        Set the form fields for every key in the form_field_dict.

        Params:
          form_field_dict -- a dictionary created by get_form_field_dict
          parent_key -- the key for the previous key in the recursive call
          field_type -- used to determine what kind of field we are setting
        """
        for form_key, field_value in form_field_dict.iteritems():
            form_key = make_key(parent_key, form_key) if parent_key is not None else form_key
            if isinstance(field_value, tuple):

                set_list_class = False
                base_key = form_key

                # Style list fields
                if ListField in (field_value.field_type, field_type):

                    # Nested lists/embedded docs need special care to get
                    # styles to work out nicely.
                    if parent_key is None or ListField == field_value.field_type:
                        if field_type != EmbeddedDocumentField:
                            field_value.widget.attrs['class'] += ' listField {0}'.format(form_key)
                        set_list_class = True
                    else:
                        field_value.widget.attrs['class'] += ' listField'

                    # Compute number value for list key
                    list_keys = [field_key for field_key in self.form.fields.keys()
                                           if has_digit(field_key)]

                    key_int = 0
                    while form_key in list_keys:
                        key_int += 1
                    form_key = make_key(form_key, key_int)

                if parent_key is not None:

                    # Get the base key for our embedded field class
                    valid_base_keys = [model_key for model_key in self.model_map_dict.keys()
                                                 if not model_key.startswith("_")]
                    while base_key not in valid_base_keys and base_key:
                        base_key = make_key(base_key, exclude_last_string=True)

                    # We need to remove the trailing number from the key
                    # so that grouping will occur on the front end when we have a list.
                    embedded_key_class = None
                    if set_list_class:
                        field_value.widget.attrs['class'] += " listField".format(base_key)
                        embedded_key_class = make_key(field_key, exclude_last_string=True)

                    field_value.widget.attrs['class'] += " embeddedField"

                    # Setting the embedded key correctly allows to visually nest the
                    # embedded documents on the front end.
                    if base_key == parent_key:
                        field_value.widget.attrs['class'] += ' {0}'.format(base_key)
                    else:
                        field_value.widget.attrs['class'] += ' {0} {1}'.format(base_key, parent_key)

                    if embedded_key_class is not None:
                        field_value.widget.attrs['class'] += ' {0}'.format(embedded_key_class)

                default_value = self.get_field_value(form_key)

                # Style embedded documents
                if isinstance(default_value, list) and len(default_value) > 0:
                    key_index = int(form_key.split("_")[-1])
                    new_base_key = make_key(form_key, exclude_last_string=True)

                    for list_value in default_value:
                        # Note, this is copied every time so each widget gets a different class
                        list_widget = deepcopy(field_value.widget)
                        new_key = make_key(new_base_key, unicode(key_index))
                        list_widget.attrs['class'] += " {0}".format(make_key(base_key, key_index))
                        self.set_form_field(list_widget, field_value.document_field, new_key, list_value)
                        key_index += 1
                else:
                    self.set_form_field(field_value.widget, field_value.document_field,
                                        form_key, default_value)

            elif isinstance(field_value, dict):
                self.set_form_fields(field_value, form_key, field_value.get("_field_type", None))

    def set_form_field(self, widget, model_field, field_key, default_value):
        """
        Parmams:
            widget -- the widget to use for displyaing the model_field
            model_field -- the field on the model to create a form field with
            field_key -- the name for the field on the form
            default_value -- the value to give for the field
                             Default: None
        """
        # Empty lists cause issues on form validation
        if default_value == []:
            default_value = None

        if widget and isinstance(widget, forms.widgets.Select):
            self.form.fields[field_key] = forms.ChoiceField(label=model_field.name,
                                                            required=model_field.required,
                                                            widget=widget)
        else:
            field_class = get_form_field_class(model_field)
            self.form.fields[field_key] = field_class(label=model_field.name,
                                                      required=model_field.required,
                                                      widget=widget)

        if default_value is not None:
            if isinstance(default_value, Document):
                # Probably a reference field, therefore, add id
                self.form.fields[field_key].initial = getattr(default_value, 'id', None)
            else:
                self.form.fields[field_key].initial = default_value
        else:
            self.form.fields[field_key].initial = getattr(model_field, 'default', None)

        if isinstance(model_field, ReferenceField):
            self.form.fields[field_key].choices = [(unicode(x.id), get_document_unicode(x))
                                                    for x in model_field.document_type.objects.all()]
            # Adding in blank choice so a reference field can be deleted by selecting blank
            self.form.fields[field_key].choices.insert(0, ("", ""))

        elif model_field.choices:
            self.form.fields[field_key].choices = model_field.choices

        for key, form_attr in CHECK_ATTRS.items():
            if hasattr(model_field, key):
                value = getattr(model_field, key)
                setattr(self.form.fields[field_key], key, value)

    def get_field_value(self, field_key):
        """
        Given field_key will return value held at self.model_instance.  If
        model_instance has not been provided will return None.
        """

        def get_value(document, field_key):
            # Short circuit the function if we do not have a document
            if document is None:
                return None

            current_key, new_key_array = trim_field_key(document, field_key)
            key_array_digit = int(new_key_array[-1]) if new_key_array and has_digit(new_key_array) else None
            new_key = make_key(new_key_array)

            if key_array_digit is not None and len(new_key_array) > 0:
                # Handleing list fields
                if len(new_key_array) == 1:
                    return_data = document._data.get(current_key, [])
                elif isinstance(document, BaseList):
                    return_list = []
                    if len(document) > 0:
                        return_list = [get_value(doc, new_key) for doc in document]
                    return_data = return_list
                else:
                    return_data = get_value(getattr(document, current_key), new_key)

            elif len(new_key_array) > 0:
                return_data = get_value(document._data.get(current_key), new_key)
            else:
                # Handeling all other fields and id
                return_data = (document._data.get(None, None) if current_key == "id" else
                              document._data.get(current_key, None))
            return return_data

        if self.is_initialized:
            return get_value(self.model_instance, field_key)
        else:
            return None
