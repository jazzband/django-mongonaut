""" Widgets for mongonaut forms"""

from django import forms

from mongoengine.base import ObjectIdField
from mongoengine.fields import BooleanField
from mongoengine.fields import DateTimeField
from mongoengine.fields import EmbeddedDocumentField
from mongoengine.fields import ListField
from mongoengine.fields import ReferenceField


def get_widget(field, disabled=False):
    
    if isinstance(field, ListField) or \
        isinstance(field, EmbeddedDocumentField):
        return None
    
    attrs={}
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

    return forms.TextInput(attrs=attrs)