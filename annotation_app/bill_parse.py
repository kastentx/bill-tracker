import re
import bs4
import requests


def get_history(chamber, number):
  # TODO temporarily hardcoded
  chamber = "SB"

  if not number.isalnum():
    None
  # Queries only senate bills in legislative session 84R
  url = "http://www.capitol.state.tx.us/BillLookup/History.aspx?LegSess=84R&Bill=" + chamber + number
  #this suffix changes depending on what stage the bill is at. we could give them an option

  res = requests.get(url)
  if not res.status_code == requests.codes.ok:
    return None

  html = bs4.BeautifulSoup(res.text)
  td = html.find('td', {'id': 'cellSubjects'}).getText()
  regex = re.compile(".*?\((.*?)\)")
  # Find all the strings between (...) - parenthesis
  result = re.findall(regex, td)

  # Delete the content between the parenthesis
  for par in result:
      td = td.replace(par, "")

  subjects_list = td.split("()")
  # Skip last element (it's an empty string anyway)
  subjects_list = subjects_list[:len(subjects_list)-1]
  return subjects_list


class Bill_Import():
    def __init__(self):
      #some commit 
        #needs input of str for bill number and a bool for issenate or ishouse
        self.bill_number = str
        self.issenate = True
        self.ishouse = False
        self.url = {'billurl' : ['http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/','.htm'],
                    'sections' : ["http://www.capitol.state.tx.us/BillLookup/",".aspx?LegSess=84R&Bill="]}
        self.endchar = ["E", "S", "H", "I", "F"]
        self.rawauthors = 'string'
        self.rawhistory = 'string'

        #outside vars
        self.billtext = list()
        self.subjects = list()
        self.authors = list()
        self.coauthors = list()
        self.cosponsors = list()
        self.sponsors = list()
    def set_bill_num(self, num):
        if not num.isalnum():
            print('error must be a number')
        else:
            self.bill_number = num
    def get_bill_num(self):
        return self.bill_number
    #function for setting if the bill is senate or house
    def set_sen_rep(self,sen,rep):
        if sen == rep:
            print('Bill must originate in either house or senate')
        elif sen:
            self.issenate = True
        else:
            self.ishouse = True

    def pull_billtext(self):
        if self.issenate:
            chamber = 'SB'
        else:
            chamber = 'HB'
        x = 0
        while x < 5:
            path = self.url['billurl'][0]+  chamber + self.bill_number.zfill(5) + self.endchar[x] + self.url['billurl'][1]
            x += 1
            res = requests.get(path)
            if not res.status_code == requests.codes.ok:
                print('not a vaild bill!')
                break
            html = bs4.BeautifulSoup(res.text)
            clean_text = html.get_text()

              # this is actually a list of sentences
            sentence_list = clean_text.split('.')
            span_text = ""
            span_id = 1

            for sentence in sentence_list:
              modified_sentence = sentence.replace('\n',"").replace('\t',"").replace('\xa0',"").replace('\r',"")
              span = '<span id="' + str(span_id) + '">' + modified_sentence + '</span>'
              span_text += span
              span_id += 1

            self.billtext.append(span_text)

    def pull_history(self):
        if self.issenate:
            chamber = 'SB'
        else:
            chamber = 'HB'
        path = self.url['sections'][0]+'History'+self.url['sections'][1]+chamber+self.bill_number
        rawhtml = requests.get(path)
        bhistory = bs4.BeautifulSoup(rawhtml.text)
        self.rawhistory = bhistory

    def set_subjects(self):
        td = self.rawhistory.find('td', {'id': 'cellSubjects'}).getText()
        regex = re.compile(".*?\((.*?)\)")
        # Find all the strings between (...) - parenthesis
        result = re.findall(regex, td)

        # Delete the content between the parenthesis
        for par in result:
          td = td.replace(par, "")

        subjects_list = td.split("()")
        # Skip last element (it's an empty string anyway)
        subjects_list = subjects_list[:len(subjects_list)-1]
        self.subjects = subjects_list

    def set_authors(self):
        td = self.rawhistory.find('td', {'id': 'cellAuthors'})
        if td != None:
          td = td.getText()
          self.authors = list(td.split('|'))

    def set_coauthors(self):
        td = self.rawhistory.find('td', {'id': 'cellCoauthors'})
        if td != None:
          td = td.getText()
          self.coauthors = list(td.split('|'))

    def set_sponsors(self):
        td = self.rawhistory.find('td', {'id': 'cellSponsors'})
        if td != None:
          td = td.getText()
          self.sponsors = list(td.split('|'))

    def set_cosponsors(self):
        td = self.rawhistory.find('td', {'id': 'cellCosponsors'})
        if td != None:
          td = td.getText()
          self.cosponsors = list(td.split('|'))



