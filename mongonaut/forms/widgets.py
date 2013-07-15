# -*- coding: utf-8 -*-

""" Widgets for mongonaut forms"""

from django import forms

from mongoengine.base import ObjectIdField
from mongoengine.fields import BooleanField
from mongoengine.fields import DateTimeField
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.fields import ListField
from mongoengine.fields import ReferenceField
from mongoengine.fields import FloatField
from mongoengine.fields import EmailField
from mongoengine.fields import DecimalField
from mongoengine.fields import URLField
from mongoengine.fields import IntField
from mongoengine.fields import StringField


def get_widget(model_field, disabled=False):

    attrs = get_attrs(model_field, disabled)

    if hasattr(model_field, "max_length") and not model_field.max_length:
        return forms.Textarea(attrs=attrs)

    elif isinstance(model_field, DateTimeField):
        return forms.DateTimeInput(attrs=attrs)

    elif isinstance(model_field, BooleanField):
        return forms.CheckboxInput(attrs=attrs)

    elif isinstance(model_field, ReferenceField) or model_field.choices:
        return forms.Select(attrs=attrs)

    elif isinstance(model_field, ListField) or isinstance(model_field, EmbeddedDocumentField):
        return None

    else:
        return forms.TextInput(attrs=attrs)


def get_attrs(model_field, disabled=False):
    attrs = {}
    attrs['class'] = 'span6 xlarge'
    if disabled or isinstance(model_field, ObjectIdField):
        attrs['class'] += ' disabled'
        attrs['readonly'] = 'readonly'
    return attrs


def get_form_field_class(model_field):
    """Gets the default form field  for a mongoenigne field."""

    FIELD_MAPPING = {
        IntField: forms.IntegerField,
        StringField: forms.CharField,
        FloatField: forms.FloatField,
        BooleanField: forms.BooleanField,
        DateTimeField: forms.DateTimeField,
        DecimalField: forms.DecimalField,
        URLField: forms.URLField,
        EmailField: forms.EmailField
    }

    return FIELD_MAPPING.get(model_field.__class__, forms.CharField)
