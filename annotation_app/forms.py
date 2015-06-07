from django import forms

class BillForm(forms.Form):
  number = forms.IntegerField()
