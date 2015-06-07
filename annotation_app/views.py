import bs4
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
import requests
from annotation_app.models import Bill, Annotation, Comment
from annotation_app.forms import BillForm#, AnnotationForm, CommentForm

def index(request):
  return render(request, 'base.html')

def bill_list(request):
  bill_list = Bill.objects.all()
  context = {'bill_list': bill_list}
  return render(request, 'bill-list.html', context)

def add_bill(request):
  if request.method == 'POST':
    form = BillForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      bill = Bill()
      bill.number = data['number']

      if not str(bill.number).isalnum():
        print('error must be a number')
      # Queries only senate bills legislative session 84R
      url = "http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/SB000" + str(bill.number) + "I.htm" #this suffix changes depending on what stage the bill is at. we could give them an option
      print("url = " + url)
      print(requests)
      res = requests.get(url)
      if not res.status_code == requests.codes.ok:
        print('not a vaild bill!')

      html = bs4.BeautifulSoup(res.text)
      clean_text = html.get_text()
      print(clean_text)

      bill.save()
      return HttpResponseRedirect("/index/")
  else:
    form = BillForm()
  return render(request, 'addbill.html', {'form': form})

def get_bill_data(number):
#TODO working on it
    bill = {}
    bill[""]


def bill(request, bill_id):
  try:
    bill = Bill.objects.get(id = bill_id)
  except Bill.DoesNotExist:
    raise Http404
  annotation_list = Annotation.objects.filter(bill_id=bill)
  context = {'bill': bill, 'annotation_list': annotation_list}
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
  comment_list = Comment.objects.filter(annotation_id=annotation)
  context = {'annotation': annotation, 'comment_list': comment_list}
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
