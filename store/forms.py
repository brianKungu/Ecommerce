from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)

class CheckoutForm(forms.Form):
    street_address= forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'237 Thika'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Appartment or suit',
        'id':'address-2'
    }))
    country = CountryField(blank_label='(select)').formfield(widget=CountrySelectWidget(attrs={
        'class':'form-field form-control custom-select w-50'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-field form-control',
        'id':'zip'
    }))
    same_shipping_address= forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)