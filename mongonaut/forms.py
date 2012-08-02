import logging

from django import forms

from mongoengine.fields import Document
from mongoengine.fields import ListField
from mongoengine.fields import ReferenceField
from mongonaut.widgets import get_form_field_class
from mongonaut.widgets import get_widget
from mongonaut.widgets import ListFieldWidget

logger = logging.getLogger('mongonaut.forms')


class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)

    def clean(self):
        for field in self.fields:
            logger.debug(field)


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


def set_form_field(form, field, key, widget, initial=None):
    """Given a form, a field, widget, and a key on the form this will set the
    correct widget on the form for the given key."""
    if widget and isinstance(widget, forms.widgets.Select):
        form.fields[key] = forms.ChoiceField(
            label=field.name,
            required=field.required,
            widget=widget)
    else:
        field_class = get_form_field_class(field)
        form.fields[key] = field_class(
            label=field.name,
            required=field.required,
            widget=widget)

    if initial:
            field_initial = getattr(initial, key)
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


def document_detail_form_factory(form, document_type, initial=False):
    """ Adds document field to a form. """
    for key in document_type._fields.keys():
        field = document_type._fields[key]
        logger.debug(field.__dict__)
        logging.debug('help')
        widget = get_widget(field)

        # Reset the list field after widget assignment so we can identify
        # the field as a ListField by the widget.  Assign it the inner field
        # so Django's default feilds work as expected.
        if isinstance(field, ListField):
            field = field.field

        if widget is None:
            # EmbeddedDocumentField
            continue

        # Deal with ListField
        if isinstance(widget, ListFieldWidget):
            if initial:
                key_index = 0

                # Add each value in the list to the form so each item in the list
                # can be modified or deleted.
                for value in initial[key]:
                    class InitialItem(object):
                        pass
                    initial_list_item = InitialItem()
                    current_key = u"{0}_{1}".format(key, key_index) if key_index else key
                    setattr(initial_list_item, current_key, value)
                    set_form_field(form, field, current_key, widget, initial_list_item)
                    form.fields[key].mongofield = field
                    key_index += 1

                if not key_index:
                    set_form_field(form, field, key, widget)
            else:
                set_form_field(form, field, key, widget)

        # All non list fields
        else:
            set_form_field(form, field, key, widget, initial)

    return form
