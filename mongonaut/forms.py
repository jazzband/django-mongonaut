from django import forms

from widgets import get_widget

class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    
    
class DocumentDetailFormFactory(object):
    """ Used to generate DocumentDetailForms for the DocumentDetailView"""
    
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


class DocumentDetailForm(forms.Form):
    pass
