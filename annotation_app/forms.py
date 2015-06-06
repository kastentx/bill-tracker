from django import forms
from annotation_app.models import Bill, Comment

class BillForm(forms.Form):
  text = forms.CharField(label='text')

class AnnotationForm(forms.Form):
  bill_id = forms.HiddenInput()
  text = forms.CharField(label='text')

class CommentForm(forms.Form):
  annotation_id = forms.HiddenInput()
  text = forms.CharField(label='text')
