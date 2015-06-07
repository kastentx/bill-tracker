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

