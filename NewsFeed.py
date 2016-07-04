# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 14:34:32 2016

@author: Auditore
"""
###############################################################
#### Свой news feed на Python или Велосипеды, как они есть ####
###############################################################

import requests
import re
from bs4 import BeautifulSoup
from tkinter import *

class site:
    def __init__(self, url):
        self.url = url
        
    def html_stripper(text):
        return re.sub('<[^<]+?>', '', str(text))
        
    def raw_parser(url):
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html)
        return soup

#### Первый парсер для it-sobytie

class ItSobytie(site):
    def __init__(self, url='http://it-sobytie.ru/', end_url='hackathon'):
        site.__init__(self, url)
        self.end_url = end_url
        
    def parser(self):
        soup = site.raw_parser(self.url+self.end_url)
        self.events = {}
        
        #### берём все предстоящие события
        total = soup.findAll('ul', attrs = {'class':'event_list'})[0]
    
        for i in range(len(total.findAll('li'))): 
            # Название мероприятия
            name = total.findAll('a', attrs = {'class':'summary'})[i]
            name = site.html_stripper(name)    
            
            # ссылка
            url = re.split('href="|">',str(total.findAll('a', attrs = {'class':'summary'})[i]))
            url = self.url+url[1]
            
            # картинка
            logo_url = re.split('src="|"/>', str(total.findAll('div', attrs={'class':'event_img'})[i]))
            logo_url = self.url+logo_url[1]
            
            self.events[name] = [url, logo_url]
        
        return self.events

ItSobytie_events = ItSobytie()
ItSobytie_events = ItSobytie_events.parser() 


################################
#### Приложение для красоты ####
################################


root = Tk()
root.configure(background='#3498DB')
Label(root, text="Hackathon News", bg='#3498DB', font=20).pack(side=TOP, fill=X)
Button(root, text='Quit', 
       command=root.destroy, 
       width=5, 
       bg='#A9F5F2').pack(side=LEFT, anchor='s')

scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill=Y )

mylist = Listbox(root, yscrollcommand = scrollbar.set, 
                 background="#E0E6F8",selectbackground="#A9F5F2",highlightcolor="#A9F5F2")
mylist.config(width=0)
for name in ItSobytie_events:
   mylist.insert(END, "")
   mylist.insert(END, name, ItSobytie_events[name][0])
   

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()
    
