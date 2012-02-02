import logging

from django import forms

from mongoengine.fields import Document, EmbeddedDocumentField, ListField, ReferenceField
from mongonaut.widgets import get_widget

logger = logging.getLogger('mongonaut.forms')

class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)


class DocumentDetailForm(forms.Form):
    pass
    
CHECK_ATTRS = dict(
        required='required',
        help_text='help_text',
        name='name'
    )

def get_document_unicode(document):
    try:
        return document.__unicode__()
    except AttributeError:
        return unicode(document)

def document_detail_form_factory(form, document_type, initial=False):
    """ Adds document field to a form. """    
    for key in document_type._fields.keys():
        field = document_type._fields[key]
        logger.debug(field.__dict__)
        logging.debug('help')
        widget = get_widget(field)
        if isinstance(widget, forms.widgets.Select):
            form.fields[key] = forms.ChoiceField(
                key, 
                required=field.required,
                widget=widget)            
        else:
            form.fields[key] = forms.CharField(
                key, 
                required=field.required,
                widget=widget)
        if initial:

            field_initial =   getattr(initial, key)
            if isinstance(field_initial, Document):
                # probably a reference field so we add some choices
                # TODO - does this actually work? Need tests and test coverage!!!
                form.fields[key].initial = field_initial.id
                form.fields[key].choices = [(unicode(x.id), get_document_unicode(x)) for x in type(field_initial).objects.all()]
            else:
                form.fields[key].initial = field_initial

        if form.fields[key].initial is None and isinstance(field, ReferenceField):
            form.fields[key].choices = [(unicode(x.id), get_document_unicode(x)) for x in field.document_type.objects.all()]
            
        
        for field_key, form_attr in CHECK_ATTRS.items():
            if hasattr(field, field_key):
                value = getattr(field, field_key)
                setattr(form.fields[key], field_key, value)

        # used as a handy reference field
        form.fields[key].mongofield = field
            
    return form


