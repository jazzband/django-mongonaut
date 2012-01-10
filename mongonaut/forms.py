from django import forms

class DocumentListForm(forms.Form):
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)