# -*- coding: utf-8 -*-
from django.forms.formsets import BaseFormSet
from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()


@register.simple_tag()
def get_document_value(document, key):
    return getattr(document, key)