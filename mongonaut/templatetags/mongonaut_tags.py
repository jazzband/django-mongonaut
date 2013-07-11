# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse

from django.utils.safestring import mark_safe

from bson.objectid import ObjectId
from mongoengine import Document
from mongoengine.fields import URLField

register = template.Library()


@register.simple_tag()
def get_document_value(document, key):
    value = getattr(document, key)
    if isinstance(value, ObjectId):
        return value

    if isinstance(document._fields.get(key), URLField):
        return mark_safe("""<a href="{0}">{1}</a>""".format(value, value))

    if isinstance(value, Document):
        app_label = value.__module__.replace(".models", "")
        document_name = value._class_name
        url = reverse("document_detail", kwargs={'app_label': app_label, 'document_name': document_name, 'id': value.id})
        return mark_safe("""<a href="{0}">{1}</a>""".format(url, value.__unicode__()))

    return value
