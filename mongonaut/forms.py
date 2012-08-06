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


def set_form_field(form, field, key, widget, initial=None, field_attrs={}):
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

    # form.fields[key].initial is None and  <-- Note this was added to the boolean expression below previously
    if isinstance(field, ReferenceField):
        form.fields[key].choices = [(unicode(x.id), get_document_unicode(x)) for x in field.document_type.objects.all()]
        form.fields[key].choices.insert(0, ("", ""))  # Do not force a choice upon the user

    for field_key, form_attr in CHECK_ATTRS.items():
        if hasattr(field, field_key):
            value = getattr(field, field_key)
            setattr(form.fields[key], field_key, value)

    # used as a handy reference field
    form.fields[key].mongofield = field


def document_detail_form_factory(form, document_type, initial=False, post_data={}):
    """ Adds document field to a form. """
    post_data_keys = [key for key in post_data.keys()]
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

        if isinstance(widget, ListFieldWidget):

            def create_list_item(form, field, widget, key, key_index, value):
                """Used to create the form field for each element in the list.
                   Returns the last name it used for the field name.
                """
                # Need this class so we can set the initial value for a field on the form
                class InitialItem(object):
                    pass
                initial_list_item = InitialItem()
                current_key = u"{0}_{1}".format(key, key_index) if key_index else key
                setattr(initial_list_item, current_key, value)
                setattr(field, 'is_list_field', True)
                set_form_field(form, field, current_key, widget, initial_list_item)
                return current_key

            # Add the class to the widget so JS can dynamically add list fields
            widget.attrs['class'] = widget.attrs['class'] + " listField {0}".format(key)

            # Keep track of keys already on the form so we know what to add from the POST data
            keys_to_add = [post_key for post_key in post_data_keys if post_key.startswith(key)]
            keys_added = []
            key_index = 0

            # If we have initial data we need to process the data differently.  An existing document
            # will have some fields already filled out.
            if initial:
                generated_key = None  # This is the key created

                for value in initial[key]:

                    # Generate the id for the new field that will be added to the form
                    generated_key = create_list_item(form, field, widget, key, key_index, value)

                    # Need to know what keys already existed for the mongo document
                    keys_added.append(generated_key)
                    key_index += 1

                # Only set fields that were posted and did not already exist on the document.
                for add_key in keys_to_add:
                    if add_key not in keys_added:
                        create_list_item(form, field, widget, key, key_index, post_data[add_key])
                        key_index += 1
            else:
                if not keys_to_add:
                    set_form_field(form, field, key, widget)
                else:
                    # Set the fields on the document from the posted variables
                    for add_key in keys_to_add:
                        if add_key not in keys_added:
                            create_list_item(form, field, widget, key, key_index, post_data[add_key])
                            key_index += 1

        # All other none list fields or embedded document fields
        else:
            set_form_field(form, field, key, widget, initial)

    return form
