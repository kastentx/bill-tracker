
import re
bill=open('bill.txt', encoding='utf-8')
#print(bill.read())
parse_this=bill.read()


#q2 = re.compile("^"+"/./")#searches for periods
#periods = q2.search(parse_this)

period=parse_this.split('.')
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