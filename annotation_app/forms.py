from django import forms

class BillForm(forms.Form):
  number = forms.IntegerField()

class BillAddForm(forms.Form):
  text = forms.CharField(label='text')

class BillEditForm(BillAddForm):
  id = forms.HiddenInput()

class AnnotationAddForm(forms.Form):
  bill_id = forms.HiddenInput()
  text = forms.CharField(label='text')

class AnnotationEditForm(AnnotationAddForm):
  id = forms.HiddenInput()

class CommentAddForm(forms.Form):
  annotation_id = forms.HiddenInput()
  text = forms.CharField(label='text')

class CommentEditForm(CommentAddForm):
  id = forms.HiddenInput()

# Deprecated

class AnnotationForm(AnnotationAddForm):
  pass

class CommentForm(CommentAddForm):
  pass
