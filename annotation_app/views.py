from django.shortcuts import render, redirect
from annotation_app.models import Bill, Annotation, Comment
from annotation_app.forms import BillForm#, AnnotationForm, CommentForm

def index(request):
  return render(request, 'base.html')

def add_bill(request):
  if request.method == 'POST':
    form = BillForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      r = Bill()
      r.text = data['text']
      r.save()
      #return redirect(recipe_list)
  else:
    form = BillForm()
  return render(request, 'addbill.html', {'form': form})
