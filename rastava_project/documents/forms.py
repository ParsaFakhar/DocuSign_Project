from django import forms


class ContractForm(forms.Form):
    recipient_name = forms.CharField(max_length=100)
    recipient_email = forms.EmailField()
    # signing_place = forms.CharField(max_length=100)
