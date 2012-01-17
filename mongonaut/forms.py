from django import forms

from mongoengine.fields import EmbeddedDocumentField, ListField
from mongonaut.widgets import get_widget



class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    
    
class DocumentDetailFormFactory(object):
    """ Used to generate DocumentDetailForms for the DocumentDetailView
        TODO: Prolly nix
    """
    
    def __init__(self, document, document_type):
        
        self.document_type
        self.document = document
        self.form = DocumentDetailForm()
        
        for key in sorted([x for x in self.document_type._fields.keys() if x != 'id']):
            # TODO - skip EmbeddedDocumentField and ListField for now
            if isinstance(self.document._fields[key], EmbeddedDocumentField):            
                continue
            if isinstance(self.document._fields[key], ListField):                                
                continue
            self.form.fields[key].append(
                get_widget('TODO - assign value')
            )

def document_detail_form_initial(form, document_type, document):
    """ Adds document field to a form. Not sure what to call this but Factory is not it."""
    for key in sorted([x for x in document_type._fields.keys() if x != 'id']):
        if isinstance(document_type._fields[key], EmbeddedDocumentField):            
            continue
        if isinstance(document_type._fields[key], ListField):                                
            continue
        form.fields[key] = forms.CharField(key, initial=getattr(document, key), widget=get_widget('TODO - assign value'))
    return form


class DocumentDetailForm(forms.Form):
    pass
