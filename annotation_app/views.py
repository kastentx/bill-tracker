from django.shortcuts import render, redirect, HttpResponseRedirect
from annotation_app.models import Bill, Annotation, Comment
from annotation_app.forms import BillForm, AnnotationForm, CommentForm

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
      return HttpResponseRedirect('/bills/%d/' % r.id)
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

def add_annotation(request):
  if request.method == 'POST':
    if 'add_for' in request.POST:
      form = AnnotationForm()
      return render(request, 'addannotation.html',
        {'form': form, 'bill_id': request.POST['add_for']})
    else:
      form = AnnotationForm(request.POST)
      if form.is_valid():
        data = form.cleaned_data
        r = Annotation()
        r.bill_id = Bill.objects.get(id = request.POST['bill_id'])
        r.text = data['text']
        r.save()
        return HttpResponseRedirect('/annotations/%d/' % r.id)
  raise Http404

def annotation(request, annotation_id):
  try:
    annotation = Annotation.objects.get(id = annotation_id)
  except Annotation.DoesNotExist:
    raise Http404
  context = {'annotation': annotation}
  return render(request, 'annotation.html', context)

def add_comment(request):
  if request.method == 'POST':
    if 'add_for' in request.POST:
      form = CommentForm()
      return render(request, 'addcomment.html',
        {'form': form, 'annotation_id': request.POST['add_for']})
    else:
      form = CommentForm(request.POST)
      if form.is_valid():
        data = form.cleaned_data
        r = Comment()
        r.annotation_id = Annotation.objects.get(id =
          request.POST['annotation_id'])
        r.text = data['text']
        r.save()
        return HttpResponseRedirect('/comments/%d/' % r.id)
  raise Http404

def comment(request, comment_id):
  try:
    comment = Comment.objects.get(id = comment_id)
  except Comment.DoesNotExist:
    raise Http404
  context = {'comment': comment}
  return render(request, 'comment.html', context)
