""" Widgets for mongonaut forms"""

from django import forms

def get_widget(field, disabled=False):
    """ TODO: Make this do something besides just character fields """
    attrs={}
    attrs['css_cls'] = 'span6'
    if disabled or (hasattr(field, "db_field") and field.db_field == '_id'):
        attrs['css_cls'] += ' disabled'
        attrs['readonly'] = 'readonly'
    

    return forms.TextInput(attrs=attrs)