import logging

from django import forms

from mongoengine.fields import EmbeddedDocumentField, ListField
from mongonaut.widgets import get_widget

logger = logging.getLogger('mongonaut.forms')

class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    

class DocumentDetailForm(forms.Form):
    pass
    
CHECK_ATTRS = dict(
        choices='choices',
        required='required',
        help_text='help_text',
        name='name'
    )


def document_detail_form_factory(form, document_type, document, initial=True):
    """ Adds document field to a form. """    
    for key in document_type._fields.keys():
        field = document_type._fields[key]
        logger.debug(field.__dict__)
        logging.debug('help')
        form.fields[key] = forms.CharField(
            key, 
            required=field.required,
            widget=get_widget(field))
        if initial:
            form.fields[key].initial = getattr(document, key)            
        
        for field_key, form_attr in CHECK_ATTRS.items():
            if hasattr(field, field_key):
                value = getattr(field, field_key)
                setattr(form.fields[key], field_key, value)
    return form


