# -*- coding: utf-8 -*-

from django.forms import Form
from mongoengine.base import TopLevelDocumentMetaclass
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.fields import ListField

from .form_mixins import MongoModelFormBaseMixin
from .form_utils import has_digit
from .form_utils import make_key
from .widgets import get_widget


class MongoModelForm(MongoModelFormBaseMixin, Form):
    """
    This class will take a model and generate a form for the model.
    Recommended use for this project only.

    Example:

    my_form = MongoModelForm(request.POST, model=self.document_type, instance=self.document).get_form()

    if self.form.is_valid():
        # Do your processing
    """

    def __init__(self, form_post_data=None, *args, **kwargs):
        """
        Overriding init so we can set the post vars like a normal form and generate
        the form the same way Django does.
        """
        kwargs.update({'form_post_data': form_post_data})
        super(MongoModelForm, self).__init__(*args, **kwargs)

    def set_fields(self):

        # Get dictionary map of current model
        if self.is_initialized:
            self.model_map_dict = self.create_document_dictionary(self.model_instance)
        else:
            self.model_map_dict = self.create_document_dictionary(self.model)

        form_field_dict = self.get_form_field_dict(self.model_map_dict)
        self.set_form_fields(form_field_dict)

    def set_post_data(self):
        # Need to set form data so that validation on all post data occurs and
        # places newly entered form data on the form object.
        self.form.data = self.post_data_dict

        # Specifically adding list field keys to the form so they are included
        # in form.cleaned_data after the call to is_valid
        for field_key, field in self.form.fields.iteritems():
            if has_digit(field_key):
                # We have a list field.
                base_key = make_key(field_key, exclude_last_string=True)

                # Add new key value with field to form fields so validation
                # will work correctly
                for key in self.post_data_dict.keys():
                    if base_key in key:
                        self.form.fields.update({key: field})

    def get_form(self):
        self.set_fields()
        if self.post_data_dict is not None:
            self.set_post_data()
        return self.form

    def create_doc_dict(self, document, doc_key=None, owner_document=None):
        """
        Generate a dictionary representation of the document.  (no recursion)

        DO NOT CALL DIRECTLY
        """
        # Get doc field for top level documents
        if owner_document:
            doc_field = owner_document._fields.get(doc_key, None) if doc_key else None
        else:
            doc_field = document._fields.get(doc_key, None) if doc_key else None

        # Generate the base fields for the document
        doc_dict = {"_document": document if owner_document is None else owner_document,
                    "_key": document.__class__.__name__.lower() if doc_key is None else doc_key,
                    "_document_field": doc_field}

        if not isinstance(document, TopLevelDocumentMetaclass) and doc_key:
            doc_dict.update({"_field_type": EmbeddedDocumentField})

        for key, field in document._fields.iteritems():
            doc_dict[key] = field

        return doc_dict

    def create_list_dict(self, document, list_field, doc_key):
        """
        Genereates a dictionary representation of the list field. Document
        should be the document the list_field comes from.

        DO NOT CALL DIRECTLY
        """
        list_dict = {"_document": document}

        if isinstance(list_field.field, EmbeddedDocumentField):
            list_dict.update(self.create_document_dictionary(document=list_field.field.document_type_obj,
                                                             owner_document=document))

        # Set the list_dict after it may have been updated
        list_dict.update({"_document_field": list_field.field,
                          "_key": doc_key,
                          "_field_type": ListField,
                          "_widget": get_widget(list_field.field),
                          "_value": getattr(document, doc_key, None)})

        return list_dict

    def create_document_dictionary(self, document, document_key=None, owner_document=None):
        """
        Given document generates a dictionary representation of the document.
        Includes the widget for each for each field in the document.
        """
        doc_dict = self.create_doc_dict(document, document_key, owner_document)

        for doc_key, doc_field in doc_dict.iteritems():
            # Base fields should not be evaluated
            if doc_key.startswith("_"):
                continue

            if isinstance(doc_field, ListField):
                doc_dict[doc_key] = self.create_list_dict(document, doc_field, doc_key)

            elif isinstance(doc_field, EmbeddedDocumentField):
                doc_dict[doc_key] = self.create_document_dictionary(doc_dict[doc_key].document_type_obj,
                                                                    doc_key)
            else:
                doc_dict[doc_key] = {"_document": document,
                                     "_key": doc_key,
                                     "_document_field": doc_field,
                                     "_widget": get_widget(doc_dict[doc_key], getattr(doc_field, 'disabled', False))}

        return doc_dict
