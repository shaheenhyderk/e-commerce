from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control mb-3'
            })
