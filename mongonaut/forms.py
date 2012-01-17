from django import forms

from mongoengine.fields import EmbeddedDocumentField, ListField
from mongonaut.widgets import get_widget

class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)

def document_detail_form_initial(form, document_type, document):
    """ Adds document field to a form. Not sure what to call this but Factory is not it.
    Handle during GET """    
    for key in sorted([x for x in document_type._fields.keys() if x != 'id']):
        if isinstance(document_type._fields[key], EmbeddedDocumentField):            
            continue
        if isinstance(document_type._fields[key], ListField):                                
            continue
        form.fields[key] = forms.CharField(key, initial=getattr(document, key), widget=get_widget('TODO - assign value'))
    return form

def document_detail_form_process(form, document_type, document, request):
    """ Handle during POST """
    for key in sorted([x for x in document_type._fields.keys() if x != 'id']):
        if isinstance(document_type._fields[key], EmbeddedDocumentField):            
            continue
        if isinstance(document_type._fields[key], ListField):                                
            continue
        form.fields[key] = forms.CharField(key, widget=get_widget('TODO - assign value'))
        
        
    



class DocumentDetailForm(forms.Form):
    pass
