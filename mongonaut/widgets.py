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


class ListFieldWidget(object):
    """A custom widget for use with the mongoengine ListField."""
    pass


def get_widget(field, disabled=False):

    if isinstance(field, EmbeddedDocumentField):
        return None

    attrs = {}
    attrs['class'] = 'span6 xlarge'
    if disabled or isinstance(field, ObjectIdField):
        attrs['class'] += ' disabled'
        attrs['readonly'] = 'readonly'

    if hasattr(field, "max_length") and not field.max_length:
        return forms.Textarea(attrs=attrs)

    if isinstance(field, DateTimeField):
        return forms.DateTimeInput(attrs=attrs)

    if isinstance(field, BooleanField):
        return forms.CheckboxInput(attrs=attrs)

    if isinstance(field, ReferenceField):
        return forms.Select(attrs=attrs)

    if isinstance(field, ListField):
        new_widget = get_widget(field.field, disabled)

        if new_widget is None:
            return None

        class InternalListFieldWidget(new_widget.__class__, ListFieldWidget):
            pass

        return InternalListFieldWidget(attrs=attrs)
    return forms.TextInput(attrs=attrs)


MAPPING = {
    IntField: forms.IntegerField,
    StringField: forms.CharField,
    FloatField: forms.FloatField,
    BooleanField: forms.BooleanField,
    DateTimeField: forms.DateTimeField,
    DecimalField: forms.DecimalField,
    URLField: forms.URLField,
    EmailField: forms.EmailField
}


def get_form_field_class(field):
    return MAPPING.get(field.__class__, forms.CharField)
