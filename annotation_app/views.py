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

def bill(request, bill_id):
  try:
    bill = Bill.objects.get(id = bill_id)
  except Bill.DoesNotExist:
    raise Http404
  context = {'bill': bill}
  return render(request, 'bill.html', context)