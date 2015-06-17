# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:04:34 2015

@author: Deepti Boddapati
/deeptiboddapati
"""
import bs4, re, itertools, collections

class html_cleanup():
    def __init__(self):
        self.text = ''
        self.sec = re.compile("\A(SECTION)")
        self.sec1 =  re.compile("\A(Sec)")
        self.sec3 = re.compile("\A(SUBCHAPTER)")
        self.sec4 = re.compile("\A(\(.\))(?!\s?\(.\))")
        self.regcheck = [[self.sec, 'SECTION', "p" ], [self.sec1, "Sec", 'p' ],[self.sec3,"Subchapter", "p"],[self.sec4, "list", "li" ]]
        self.taglist = ['a']
        self.title = ''

    def set_text(self, text = 'a'):   
        self.text = bs4.BeautifulSoup(text)
        a = list()
        for ele in self.text.find_all(True):
            a.append(ele.name)
        self.taglist = list(set(a))

    def remove_space(self, tag):
        for x in (list(self.text(tag)[0].next_siblings) + list(self.text(tag)[0].previous_siblings)):
            if type(x) == bs4.element.NavigableString:
                x.extract()

    def remove_empty_tag(self):  
        for x in range(len(self.taglist)):
            i = 0
            # removes the tags with just space in them.
            while i < (len(self.text(self.taglist[x]))):
                if self.text(self.taglist[x])[i].getText().isspace():
                    self.text(self.taglist[x])[i].decompose()
                else:
                    i +=1


    def remove_title(self):
        self.title = re.sub(r'(\s\s+)',r' ', self.text('title')[0].extract().get_text())
        #gets the second table in text which contains the bill. 
        self.text = self.text('table')[1].extract()
        #gets the first sentence of the bill.
        for x in self.text('td'):
            chkstring = x.get_text() #TODO ask mark if he wants the text extracted.
            b = re.search('[.]',chkstring)
            #replaces weird spaces with normal spacing. 
            self.title += re.sub(r'(\s\s+)',r' ', chkstring) 
            if b is not None:#stops the loop when a period is found. 
                break

    def consolidate_tag(self,rem, tag):
        if rem == 'parent':
            self.rm_tag_str_parent(tag)
        elif rem == 'sibling same name':
            self.rm_tag_str_same_sib(tag)
        elif rem == 'sibling different name':
            self.rm_tag_str_dif_sib(tag)
        else:
            print('Must specify how you want to remove the tag.')


    def rm_tag_str_parent(self,tag):
        for i in self.text(tag):
            i.unwrap()

    def rm_tag_str_dif_sib(self,tag):
        for y in self.text(tag): #removes tr tags and puts their strings into other tags.
            firstele = True
            while y.previous_sibling and y.previous_sibling.name != tag:
                firstele = False
                m = y.previous_sibling
                y.extract()
                string =list(y.contents)
                for q in string:
                    m.append(q)
            if firstele:
                y.name = 'p'

    def rm_tag_str_same_sib(self, tag):
        for i in self.text(tag):
            #find out if tag has siblings. 
            if i.find_next_siblings():
                # if there are siblings see if their tag is the same
                for x in i.find_next_siblings():
                    # if the name is the the same then remove the text and place inside tag.
                    if x.name == i.name:
                        i.append(x.extract().get_text())

    def add_tags(self, tag):
        #find each expression and add the classes in the set to it.
        for x in self.regcheck:#TODO google double for
            for i in self.text(tag):
                #check what the first word is
                if re.search(x[0], list(i.stripped_strings)[0]):
                    i.name = x[2]
                    i['class'] = x[1]




def htmltext(text):
    ttobj = html_cleanup()
    #set text
    ttobj.set_text(text)
    #remove empty tag
    ttobj.remove_empty_tag()
    #consolidate tag same sib u
    ttobj.consolidate_tag('sibling same name', 'u')
    #consolidate tag parent td
    ttobj.consolidate_tag('parent', 'td')
    #remove title
    ttobj.remove_title()
    #remove space
    ttobj.remove_space('tr')
    #add tags
    ttobj.add_tags('tr')
    #consolidate tag diff sib tr
    ttobj.consolidate_tag('sibling different name', 'tr')
    return ttobj.text