from django import forms

class BillForm(forms.Form):
  number = forms.IntegerField()

class BillAddForm(forms.Form):
  text = forms.CharField(label='text')

class BillEditForm(BillAddForm):
  id = forms.HiddenInput()

class AnnotationAddForm(forms.Form):
  user = forms.CharField(label='user')
  bill = forms.HiddenInput()
  text = forms.CharField(label='text')
  quote = forms.CharField(label='quote')

  ranges_start_offset = forms.IntegerField(label='ranges_start_offset')
  ranges_end_offset = forms.IntegerField(label='ranges_end_offset')

  tags = forms.CharField(label='tags')

  permissions_read = forms.CharField(label='permissions_read')

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
