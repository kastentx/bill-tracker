import bs4
from django.core import serializers
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
from annotation_app.bill_parse import Bill_Import
from django.core import serializers
 #get_history,

from annotation_app.models import Bill, Annotation, Comment, Senator, Subject
from annotation_app.forms import AnnotationAddForm, AnnotationEditForm, CommentAddForm, BillForm, BillEditForm
import json


def index(request):
  return render(request, 'base.html')

def bill_list(request):
  return render(request, 'bill-list.html')

def subject_list(request):
  return render(request, 'subject-list.html')

def author_list(request):
  return render(request, 'author-list.html')

def add_bill(request):
  if request.method == 'POST':
    form = BillForm(request.POST)

    if form.is_valid():
      data = form.cleaned_data
      bill_num = data["number"]
      bill = Bill.objects.filter(number=bill_num)
      # If you find bill in the database, it is the first element in QuerySet
      if bill:
          bill = bill[0]
      # If bill is not in the database, pull it from TLO website
      if not bill:
        data = form.cleaned_data
        bill = Bill()
        bill.number = data['number']
        bill_import = Bill_Import()
        bill_import.set_bill_num(str(bill.number))
        bill_import.pull_billtext()
        bill_list = bill_import.billtext
        bill.text = Bill.serialize(bill_list)
        bill_import.pull_history()
        bill_import.set_data()
        bill.authors = Bill.serialize(bill_import.authors)
        bill.coauthors = Bill.serialize(bill_import.coauthors)
        bill.subjects = Bill.serialize(bill_import.subjects)
        bill.cosponsors = Bill.serialize(bill_import.cosponsors)
        bill.sponsors = Bill.serialize(bill_import.sponsors)
        bill.save()

        save_authors(bill, bill_import.authors)
        save_subjects(bill, bill_import.subjects)

      if 'format' in request.POST:
        return HttpResponse(serializers.serialize(request.POST['format'],
          [bill]))
      else:
        return HttpResponseRedirect('/bills/%d/' % bill.id)
  else:
    form = BillForm()
  return render(request, 'addbill.html', {'form': form})

def save_authors(bill, authors):

  for author in authors:
      senator = Senator.objects.filter(name=author)
      # If this senator is not in the db, add her/him
      if not senator:
        senator = Senator()
        senator.name = author
        senator.committee = "comittee" # TODO fix hardcode
        senator.is_chair = False # TODO fix hardcode
        senator.save()
        # Associate this senator with imported bill
        senator.bills.add(bill)
        senator.save()

def save_subjects(bill, subjects):

  for subject_name in subjects:
    subject = Subject.objects.filter(name=subject_name)
    # If this subject is not in the db, add her/him
    if not subject:
      subject = Subject()
      subject.name = subject_name
      subject.save()
      # Associate this subject with imported bill
      subject.bills.add(bill)
      subject.save()

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


@ensure_csrf_cookie
def bill(request, bill_id):
  try:
    bill = Bill.objects.get(id = bill_id)
  except Bill.DoesNotExist:
    raise Http404
  # annotation_list = bill.annotation_set.all()
  bill.text = text_frontend(bill.text)
  authors = Bill.deserialize(bill.authors)
  subjects = Bill.deserialize(bill.subjects)
  context = {'bill': bill, 'authors': authors, 'subjects': subjects }#, 'annotation_list': annotation_list}
  return render(request, 'bill.html', context)

@ensure_csrf_cookie
def author(request, author_id):
  try:
    author = Senator.objects.get(id = author_id)
  except Senator.DoesNotExist:
    raise Http404
  context = {'author': author}
  return render(request, 'author.html', context)

def get_bill_list(request):
  #TODO optimize
  data = serializers.serialize("json", Bill.objects.all())
  print(data)
  return HttpResponse(data)

def get_subject_list(request):
  #TODO optimize
  data = serializers.serialize("json", Subject.objects.all())
  print(data)
  return HttpResponse(data)

def get_author_list(request):
  #TODO optimize
  data = serializers.serialize("json", Senator.objects.all())
  print(data)
  return HttpResponse(data)

def get_author_bills(request):
  author_id = request.GET.get("id")
  #TODO optimize
  data = Senator.objects.get(id=author_id).bills.all()
  print(data)
  data = serializers.serialize("json", data)
  print(data)
  return HttpResponse(data)


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

def annotations(request):
  if request.method == 'GET':
    bill_id = re.search(r'bills/(?P<bill_id>\d+)/$',
      request.META['HTTP_REFERER']).group(1)
    bill = Bill.objects.get(id = bill_id)
    annotations = bill.annotation_set.all()
    annotation_list = []
    counter = 1
    for annotation in annotations:
      data = {}
      data['id'] = annotation.id
      data['user'] = annotation.user or 'demoUser'
      created = annotation.created
      data['data_creacio'] = unix_time(created) if created else counter
      counter += 1000
      data['text'] = annotation.text
      data['quote'] = annotation.quote
      data['ranges'] = [{
        'startOffset': annotation.ranges_start_offset,
        'endOffset': annotation.ranges_end_offset,
        'start': '',
        'end': ''
      }]
      data['tags'] = json.loads(annotation.tags) if annotation.tags else []
      read_perm = annotation.permissions_read
      data['permissions'] = {
        'read': json.loads(read_perm) if read_perm else [data['user']],
        'update': [data['user']],
        'delete': [data['user']],
        'admin': [data['user']]
      }
      annotation_list.append(data)
    return HttpResponse(json.dumps(annotation_list))

  elif request.method == 'POST':
    input_data = json.loads(request.body.decode("utf-8"))
    input_data['tags'] = json.dumps(input_data['tags'])
    input_data['ranges_start_offset'] = input_data['ranges'][0]['startOffset']
    input_data['ranges_end_offset'] = input_data['ranges'][0]['endOffset']
    input_data['permissions_read'] = \
      json.dumps(input_data['permissions']['read'])
    form = AnnotationAddForm(input_data)

    if form.is_valid():
      data = form.cleaned_data
      annotation = Annotation()
      annotation.user = data['user']
      bill = Bill.objects.get(id = input_data['bill_id'])
      annotation.bill = bill
      annotation.text = data['text']
      annotation.quote = data['quote']
      annotation.ranges_start_offset = data['ranges_start_offset']
      annotation.ranges_end_offset = data['ranges_end_offset']
      annotation.tags = data['tags']
      annotation.permissions_read = data['permissions_read']
      annotation.save()

      return HttpResponse('{"id":'+ str(annotation.id) +'}')
    else:
      return HttpResponse(status=400)

# {'quote': 'BILL', 'text': 'Clinton', 'permissions': {'delete': ['demoUser'],
# 'read': [], 'update': ['demoUser'], 'admin': ['demoUser']},
# 'user': 'demoUser', 'data_creacio': 1434156917763, 'ranges':
# [{'endOffset': 83, 'end': '', 'startOffset': 79, 'start': ''}],
# 'tags': ['Former', 'president'], 'bill_id': 1, 'id': 1434156917830}

def annotation(request, annotation_id):
  if request.method == 'PUT':
    input_data = json.loads(request.body.decode("utf-8"))
    input_data['tags'] = json.dumps(input_data['tags'])
    input_data['ranges_start_offset'] = input_data['ranges'][0]['startOffset']
    input_data['ranges_end_offset'] = input_data['ranges'][0]['endOffset']
    input_data['permissions_read'] = \
      json.dumps(input_data['permissions']['read'])
    form = AnnotationEditForm(input_data)

    if form.is_valid():
      data = form.cleaned_data
      annotation = Annotation.objects.get(id = annotation_id)
      annotation.user = data['user']
      bill = Bill.objects.get(id = input_data['bill_id'])
      annotation.bill = bill
      annotation.text = data['text']
      annotation.quote = data['quote']
      annotation.ranges_start_offset = data['ranges_start_offset']
      annotation.ranges_end_offset = data['ranges_end_offset']
      annotation.tags = data['tags']
      annotation.permissions_read = data['permissions_read']
      annotation.save()

      return HttpResponse("{}")
    else:
      return HttpResponse(status=400)

  elif request.method == 'DELETE':
    try:
      annotation = Annotation.objects.get(id = annotation_id)
    except Annotation.DoesNotExist:
      raise Http404

    annotation.delete()
    return HttpResponse("{}")
  # try:
  #   annotation = Annotation.objects.get(id = annotation_id)
  # except Annotation.DoesNotExist:
  #   raise Http404
  # comment_list = Comment.objects.filter(annotation_id=annotation)
  # context = {'annotation': annotation, 'comment_list': comment_list}
  # return render(request, 'annotation.html', context)

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

@ensure_csrf_cookie
def example_client(request):
  return render(request, 'example.html')

def megalith(request):
  return render(request, 'megalith/megalith.html')

import re

# For the love of god, don't touch this!!!
def text_frontend(text):
  output = text
  output = output.split('", "')[0]
  output = re.sub('\["', '', output)

  # if re.search('</span>', output):
  #   output = output.replace('</span>', '.</span>').replace('\\',"")
  #   output = str(re.sub(r'\{.+\}\s*', '', output))
  #   return output
  # else:
  #   sentence_list = output.split('.')
  #   sentence_list.pop()
  #   span_text = ""
  #   span_id = 1

  #   for sentence in sentence_list:
  #     modified_sentence = sentence.replace('\n',"").replace('\t',"").replace('\xa0',"").replace('\r',"").replace('\\',"")
  #     span = '<span id="' + str(span_id) + '">' + modified_sentence + '.</span>'
  #     span_text += span
  #     span_id += 1

  #   return span_text
  return output

## Helper methods

import datetime
def unix_time(dt):
  naive = dt.replace(tzinfo=None)
  epoch = datetime.datetime.utcfromtimestamp(0)
  delta = naive - epoch
  return int(delta.total_seconds() * 1000)
