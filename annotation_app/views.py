import bs4
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
import requests
from annotation_app.models import Bill, Annotation, Comment
from annotation_app.forms import BillForm#, AnnotationForm, CommentForm

def index(request):
  return render(request, 'base.html')

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
  context = {'bill': bill}
  return render(request, 'bill.html', context)