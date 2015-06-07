from django import forms

class BillForm(forms.Form):
  number = forms.IntegerField()

class AnnotationForm(forms.Form):
  bill_id = forms.HiddenInput()
  text = forms.CharField(label='text')

class CommentForm(forms.Form):
  annotation_id = forms.HiddenInput()
  text = forms.CharField(label='text')
