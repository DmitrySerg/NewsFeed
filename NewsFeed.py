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
import time
from dateutil import parser
import pandas as pd

data = pd.DataFrame(columns=['name', 'url', 'date', 'date_tmstp', 'logo_url'])

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
    
    '''переводит формат "6 января 2016" в timestamp'''
    def date_convert(string):
        months = ['января', 'февраля', 'марта', 'апреля', 'мая',
                  'июня','июля','августа','сентрября','октября','ноября', 'декабря']
        month = string.split()[1]
        formatted = string.replace(month, str(months.index(month)+1))
        return parser.parse(formatted)        

        
#### Первый парсер для it-sobytie

class ItSobytie(site):
    def __init__(self, url='http://it-sobytie.ru/', end_url='hackathon'):
        site.__init__(self, url)
        self.end_url = end_url
        
    def site_parser(self):
        global data
        soup = site.raw_parser(self.url+self.end_url)
        events = {}
        
        #### берём все предстоящие события
        total = soup.findAll('ul', attrs = {'class':'event_list'})[0]
    
        for i in range(len(total.findAll('li'))): 
            # Название мероприятия
            name = total.findAll('a', attrs = {'class':'summary'})[i]
            name = site.html_stripper(name)    
            
            # дата в текстовом формате
            date = total.findAll('span', attrs={'class':'dtstart'})[i]
            date = site.html_stripper(date).strip('\n')
            
            # дата в формате timestamp
            date_tmstp = site.date_convert(date)
            
            # ссылка
            event_url = re.split('href="|">',str(total.findAll('a', attrs = {'class':'summary'})[i]))
            event_url = self.url+event_url[1]
            
            # картинка
            logo_url = re.split('src="|"/>', str(total.findAll('div', attrs={'class':'event_img'})[i]))
            logo_url = self.url+logo_url[1]
            
            events = {'name':name, 'url':event_url, 'date':date, 
                           'date_tmstp':date_tmstp, 'logo_url':logo_url}
            data = data.append(events, ignore_index = True)

'''Создаём экземпляр класса и вызываем парсер'''
ItSobytie_events = ItSobytie()
ItSobytie_events.site_parser() 


################################
#### Приложение для красоты ####
################################

import tkinter as tk

class App(tk.Tk):
    def __init__(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.configure(background='#3498DB')
        self.label = tk.Label(self, text="Hackathon News", bg='#3498DB', font=20)
        self.label.pack(side=TOP, fill=X)
                
        
        self.button = tk.Button(self, text='Quit', command=self.destroy, width=5, bg='#A9F5F2')
        
        self.button.pack(side=LEFT, anchor='s')
        
        
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack( side = RIGHT, fill=Y )
        self.mylist = tk.Listbox(self, yscrollcommand = self.scrollbar.set, 
                                     background="#E0E6F8",
                                     selectbackground="#A9F5F2",
                                     highlightcolor="#A9F5F2")
        self.mylist.config(width=0)
                
        self.update()        

    
    def update(self):
        global data
        ItSobytie_new_events = ItSobytie()
        ItSobytie_new_events.site_parser()
        
        # для отладки создаем кучу новых имён
        events = {'name':time.time(), 'url':'url', 'date':'date', 
                  'date_tmstp':'date_tmstp', 'logo_url':'logo_url'}
        data = data.append(events, ignore_index = True)
        
            
        for row in range(len(data)):
            '''проверяем, есть ли такое имя в списке, вносим, если нет'''
            if data.loc[row, 'name'] not in self.mylist.get(0, 10000):
                self.mylist.insert(END, "")
                self.mylist.insert(END, data.loc[row, 'name'], 
                                        data.loc[row, 'date'],
                                        data.loc[row, 'url'])
                self.mylist.pack( side = LEFT, fill = BOTH )
                self.scrollbar.config( command = self.mylist.yview )
            
        if True:
            self.after(3000, self.update)


app = App()
app.mainloop()


root = tk.Tk()
mylist = tk.Listbox(root, 
                                     background="#E0E6F8",
                                     selectbackground="#A9F5F2",
                                     highlightcolor="#A9F5F2")
for name in ItSobytie_events:
    mylist.insert(END, "")
    mylist.insert(END, name, ItSobytie_events[name][0], ItSobytie_events[name][1])
    mylist.pack( side = LEFT, fill = BOTH )
