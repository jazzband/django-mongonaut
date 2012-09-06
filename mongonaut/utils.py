# -*- coding: utf-8 -*-

from mongoengine.base import ObjectIdField, ValidationError
from mongoengine.fields import ReferenceField

# Used to validate object_ids.
# Called by is_valid_object_id
OBJECT_ID = ObjectIdField()


def is_valid_object_id(value):
    try:
        OBJECT_ID.validate(value)
        return True
    except ValidationError:
        return False


def translate_value(document_field, form_value):
    """
    Given a document_field and a form_value this will translate the value
    to the correct result for mongo to use.
    """
    value = form_value
    if isinstance(document_field, ReferenceField):
        value = document_field.document_type.objects.get(id=form_value) if form_value else None
    return value


def trim_field_key(document, field_key):
    """
    Returns the smallest delimited version of field_key that
    is an attribute on document.

    return (key, left_over_array)
    """
    trimming = True
    left_over_key_values = []
    current_key = field_key
    while trimming and current_key:
        if hasattr(document, current_key):
            trimming = False
        else:
            key_array = current_key.split("_")
            left_over_key_values.append(key_array.pop())
            current_key = u"_".join(key_array)

    left_over_key_values.reverse()
    return current_key, left_over_key_values
