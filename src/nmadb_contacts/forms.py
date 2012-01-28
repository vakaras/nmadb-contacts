from django import forms
from nmadb_contacts import models


class HumanForm(forms.ModelForm):
    """ Form for Human model.
    """

    def __init__(self, *args, **kwargs):
        super(HumanForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            main_address_field = self.fields['main_address']
            main_address_field.queryset = (
                    main_address_field.queryset.filter(human=instance))

    class Meta(object):
        model = models.Human
