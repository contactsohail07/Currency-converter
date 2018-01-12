from django import forms


class CurrencyForm(forms.Form):
	fr = forms.CharField(max_length=3)
	to = forms.CharField(max_length=3)
	fields = ('fr','to')
