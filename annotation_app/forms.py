from django import forms

class BillForm(forms.Form):
  text = forms.CharField(label='text')
