import bs4
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import requests
from annotation_app.bill_parse import Bill_Import
 #get_history,

from annotation_app.models import Bill, Annotation, Comment
from annotation_app.forms import AnnotationAddForm, CommentAddForm, BillForm, BillEditForm



def index(request):
  return render(request, 'base.html')

def bill_list(request):
  bill_list = Bill.objects.all()
  for bill in bill_list:
    bill.text = text_frontend(bill.text)
  context = {'bill_list': bill_list}
  return render(request, 'bill-list.html', context)

def add_bill(request):
  if request.method == 'POST':
    form = BillForm(request.POST)
    if form.is_valid():
      print("Checkpoint1")
      data = form.cleaned_data
      bill = Bill()
      bill.number = data['number']
      billsb10 = Bill_Import()
      billsb10.set_bill_num(str(bill.number))
      billsb10.pull_billtext()
      bill_list = billsb10.billtext
      bill.text = Bill.serialize(bill_list)
      print("Checkpoint3")
      billsb10.pull_history()
      print("Checkpoint4")
      billsb10.set_data()
      bill.authors = Bill.serialize(billsb10.authors)
      bill.coauthors = Bill.serialize(billsb10.coauthors)
      bill.subjects = Bill.serialize(billsb10.subjects)
      bill.cosponsors = Bill.serialize(billsb10.cosponsors)
      print("Checkpoint7")
      bill.sponsors = Bill.serialize(billsb10.sponsors)
      print('authors', Bill.deserialize(bill.authors))
      #print('billtext', Bill.deserialize(bill.text))
      print('subjects', Bill.deserialize(bill.subjects))
      print('coauthors', Bill.deserialize(bill.coauthors))
      print('sponsors', Bill.deserialize(bill.sponsors))
      print('cosponsors', Bill.deserialize(bill.cosponsors))

      ####

      bill.save()
      return HttpResponseRedirect('/bills/%d/' % bill.id)
  else:
    form = BillForm()
  return render(request, 'addbill.html', {'form': form})


def get_bill_text(number):

  if not number.isalnum():
    None
  # Queries only senate bills in legislative session 84R
  url = "http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/SB000" + number + "I.htm"
  #this suffix changes depending on what stage the bill is at. we could give them an option

  res = requests.get(url)
  if not res.status_code == requests.codes.ok:
    return None

  html = bs4.BeautifulSoup(res.text)
  clean_text = html.get_text()
  # this is actually a list of sentences
  sentence_list = clean_text.split('.')
  span_text = ""
  span_id = 0

  for sentence in sentence_list:
    modified_sentence = sentence.replace('\n',"").replace('\t',"").replace('\xa0',"").replace('\r',"")
    span = '<span id=' + str(span_id) + '>' + modified_sentence + '</span>'
    span_text += span
    span_id += 1

  return span_text


def bill(request, bill_id):
  try:
    bill = Bill.objects.get(id = bill_id)
  except Bill.DoesNotExist:
    raise Http404
  annotation_list = Annotation.objects.filter(bill_id=bill)
  bill.text = text_frontend(bill.text)
  context = {'bill': bill, 'annotation_list': annotation_list}
  return render(request, 'bill.html', context)

def add_annotation(request):
  if request.method == 'POST':
    if 'add_for' in request.POST:
      form = AnnotationAddForm()
      return render(request, 'addannotation.html',
        {'form': form, 'bill_id': request.POST['add_for']})
    else:
      form = AnnotationAddForm(request.POST)
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
      form = CommentAddForm()
      return render(request, 'addcomment.html',
        {'form': form, 'annotation_id': request.POST['add_for']})
    else:
      form = CommentAddForm(request.POST)
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


def edit_bill(request, bill_id):
  try:
    bill = Bill.objects.get(id = bill_id)
  except Bill.DoesNotExist:
    raise Http404

  if request.method == 'POST':
    form = BillEditForm(request.POST)
    if form.is_valid():
      data = form.cleaned_data
      bill.text = data['text']
      bill.save()
      return HttpResponseRedirect('/bills/%d/' % bill.id)
  else:
    form = BillEditForm(initial={'id': bill.id, 'text': bill.text})
  return render(request, 'billform.html',
    {'form': form, 'method': 'edit', 'id': bill.id})

def example_client(request):
  return render(request, 'example.html')

from django.core.serializers import serialize

def megalith(request):
  return render(request, 'megalith/megalith.html')

import re

# For the love of god, don't touch this!!!
def text_frontend(text):
  output = text
  output = output.split('", "')[0]
  output = re.sub('\["', '', output)

  if re.search('</span>', output):
    output = output.replace('</span>', '.</span>').replace('\\',"")
    output = str(re.sub(r'\{.+\}\s*', '', output))
    return output
  else:
    sentence_list = output.split('.')
    sentence_list.pop()
    span_text = ""
    span_id = 1

    for sentence in sentence_list:
      modified_sentence = sentence.replace('\n',"").replace('\t',"").replace('\xa0',"").replace('\r',"").replace('\\',"")
      span = '<span id="' + str(span_id) + '">' + modified_sentence + '.</span>'
      span_text += span
      span_id += 1

    return span_text
