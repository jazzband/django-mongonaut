""" Widgets for mongonaut forms"""

from django import forms

def get_widget(field, disabled=False):
    """ TODO: Make this do something besides just character fields """
    attrs={}
    attrs['class'] = 'span6 xlarge'
    if disabled or (hasattr(field, "db_field") and field.db_field == '_id'):
        attrs['class'] += ' disabled'
        attrs['readonly'] = 'readonly'
    
    if hasattr(field, "max_length") and not field.max_length:
        return forms.Textarea(attrs=attrs)
        
    if hasattr(field, 'document_type_obj'):
        # for ReferenceField - like <class 'articles.models.User'> on Blog
        attrs['class'] += ' disabled'
        attrs['readonly'] = 'readonly'
        
    if hasattr(field, "field"):
        # For ListField - like 'field': <mongoengine.fields.StringField object at 0x101b51810>,        
        attrs['class'] += ' disabled'
        attrs['readonly'] = 'readonly'
        

    return forms.TextInput(attrs=attrs)