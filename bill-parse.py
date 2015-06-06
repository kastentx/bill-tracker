


import requests, bs4

bill_number = input('bill number')
if not bill_number.isalnum():
    print('error must be a number')
url = "http://www.capitol.state.tx.us/tlodocs/84R/billtext/html/SB000" + bill_number + "I.htm" #this suffix changes depending on what stage the bill is at. we could give them an option
res = requests.get(url)
if not res.status_code == requests.codes.ok:
    print('not a vaild bill!')
html = bs4.BeautifulSoup(res.text)
clean_text = html.get_text()

period=clean_text.split('.')
#print (period)

index=len(period)-1
print(index)
span_list=[]
i=0
while i<= index:
    #print(period[i]+'ENDDDDDD')
    span='<span>'+period[i]+'</span>'
    print(span)
    span_list.append(span)
    #print(span_list)
    #period[i].append('</span>')
    #span+=period[i]
    i+=1

print (span_list)