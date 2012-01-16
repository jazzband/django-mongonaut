""" Widgets for mongonaut forms"""

from django import forms

def get_widget(document_type):
    """ TODO: Make this do something besides just character fields """
    return forms.TextInput