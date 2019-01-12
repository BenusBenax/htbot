#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from __future__ import print_function
import requests

import vk_api
import time
from weather import Weather
from associator import weather_asso, hello_asso, booking_asso
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import datetime 

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#from vk_api.utils import get_random_id
#date_1=datetime.date.today()+datetime.timedelta(days=1)



def date_format(start_from_cal_api): #пихаем сюда строчку от гугл апи с датой и временем события

    spl=start_from_cal_api.split('T')
    date=spl[0].split('-')
    DATE_str=str(date[2])+'-'+str(date[1])+'-'+str(date[0])
    time_1=spl[1].split('+')
    time_2=time_1[0].split(':')
    time_3=time_1[1].split(':')
    H=int(time_3[0])+int(time_2[0])
    M=int(time_3[1])+int(time_2[1])
    if M<10:
        M_str=("0"+str(M))
    else:
        M_str=str(M)
    Time=str(H)+':'+M_str
    #print(spl[1])
   # print(DATE_str,Time)
    return DATE_str

def time_format(start_from_cal_api): #пихаем сюда строчку от гугл апи с датой и временем события
    #print(",kf,kf  "+start_from_cal_api)
    spl=start_from_cal_api.split('T')
    date=spl[0].split('-')
    DATE_str=str(date[2])+'-'+str(date[1])+'-'+str(date[0])
    time_1=spl[1].split('+')
    time_2=time_1[0].split(':')
    H=time_2[0]
    M=time_2[1]
    
    Time=H+':'+M
   # print(spl[1])
    #print(Time)
    return Time 
#################################################  
def id_events_call(date_of_book):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    
    book_mass=[]
    book_mass_id=[]
    time_maxi=date_of_book+datetime.timedelta(days=1)
    #time_maxi=datetime.timedelta(days=1)
    #date_of_book_1=date_of_book +datetime.timedelta(days=1)
    
    events_result = service.events().list(calendarId='primary', timeMin=(date_of_book.isoformat()+'Z'),timeMax=(time_maxi.isoformat()+'Z'),maxResults=5, singleEvents=True,orderBy='startTime').execute()
    events = events_result.get('items', [])
    # print(events)
    #if not events:
        #print('No upcoming events found.')
        
    for event in events:
        if 'summary' not in event:
            #print('есть саммари в ивенте')
        #else:
            #print('нет саммари в ивенте')
            book_mass_id.append(event['id'])
            asdasd=event['start']
            asdas=asdasd['dateTime']
            book_mass.append(asdas)
    else:
        #print("zero events")
        book_mass.append('zero')
    
  
    book_mass.append('zero')
    return book_mass_id,book_mass

####################################################
def booking_by_eventId(event_calendar_id,name_of_user,comments):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    event = service.events().get(calendarId='primary',eventId=event_calendar_id).execute()
    #print(str(event))
    event['colorId']='11'
    event["summary"]=name_of_user
    event["description"]=comments
    created_event = service.events().update(calendarId='primary',eventId=event['id'],body=event).execute()
        


    return 1


############################################################

def get_random_id():
    return int(time.time() * 10000000)
#################################################
def get_time_buttons(t_1,t_2,t_3,t_4,t_5):
    keyboard_date = VkKeyboard(one_time=True)
    
    keyboard_date.add_button(t_1, color=VkKeyboardColor.DEFAULT)
    if t_2!="zero":
        keyboard_date.add_button(t_2, color=VkKeyboardColor.DEFAULT)
    if t_3!="zero":
        keyboard_date.add_button(t_3, color=VkKeyboardColor.DEFAULT)
    if t_4!="zero":
        if t_5!="zero":
            keyboard_date.add_line()
            keyboard_date.add_button(t_4, color=VkKeyboardColor.DEFAULT)
            keyboard_date.add_button(t_5, color=VkKeyboardColor.DEFAULT)
        else:
            keyboard_date.add_button(t_4, color=VkKeyboardColor.DEFAULT)
    
    keyboard_date.add_line()
    keyboard_date.add_button('В начало', color=VkKeyboardColor.NEGATIVE)
    keyboard_date.add_button("К выбору даты", color=VkKeyboardColor.DEFAULT)
    return keyboard_date
################################################################
def get_date_buttons(d_1,d_2,d_3,d_4):
    keyboard_date = VkKeyboard(one_time=True)
    
    keyboard_date.add_button(d_1.strftime("%d-%m-%Y"), color=VkKeyboardColor.DEFAULT)
    keyboard_date.add_button(d_2.strftime("%d-%m-%Y"), color=VkKeyboardColor.DEFAULT)
    keyboard_date.add_button(d_3.strftime("%d-%m-%Y"), color=VkKeyboardColor.DEFAULT)
    keyboard_date.add_button(d_4.strftime("%d-%m-%Y"), color=VkKeyboardColor.DEFAULT)
    keyboard_date.add_line()
    keyboard_date.add_button('В начало', color=VkKeyboardColor.NEGATIVE)
    keyboard_date.add_button("След. даты", color=VkKeyboardColor.DEFAULT)
    return keyboard_date
#####################################################
def main():
    #try:
		#vk_auth
        session = requests.Session()
        level2=[]
        level3=[]
        level4=[]
        ids=[]
        days_mass=[]
        Ids_mass=[]
    
        vk_session = vk_api.VkApi(token='42117b3a93e9f6f9bb1de66446b4856a460db93cf87bff530e62de233503df5c42c13203de0f3a0ec3cc6')#quant
        #vk_session = vk_api.VkApi(token='069d9ce67dc166da0a16c9b233575e280daa970b2884df2dec367532d5798f9c87963d600a69ca66feb60')#buhi 

        vk = vk_session.get_api()

        upload = VkUpload(vk_session)  # Для загрузки изображений
        longpoll = VkLongPoll(vk_session)
        	
        text='Вы хотите забронировать Хайтек цех ?'
        
        keyboard = VkKeyboard(one_time=True)
        keyboard_2 = VkKeyboard(one_time=True) 
		
        text_button11="Привет"
        text_button12="Бронь"
        text_button13="Погода"
        text_button21="В начало"
        text_button22="След. даты"
        text_button23=""
        text_button31="Назад"
        text_button32="Выход"
        hide_key=0 ##для каждого айди
        keyboard.add_button(text_button11, color=VkKeyboardColor.DEFAULT)
        keyboard.add_button(text_button12, color=VkKeyboardColor.DEFAULT)
        keyboard.add_button(text_button13, color=VkKeyboardColor.DEFAULT)
        keyboard.add_line()  # Переход на вторую строку
        keyboard.add_button(text_button21, color=VkKeyboardColor.NEGATIVE)
        kb_m=keyboard
        days_plus=0 
        book_date=datetime.datetime.utcnow().isoformat()
        admin_id=19132305
        
          
   
    

        for event in longpoll.listen():
       
        
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                
                #print('написал id{}: "{}"'.format(event.user_id, event.text), end=' ')
                jhg=vk.users.get(user_id=event.user_id)
                name_user=jhg[0]['first_name']+'  '+jhg[0]['last_name']
                print (name_user + " : " + event.text)
                #print(level2)
                
                if event.text==text_button21: ##в начало
                   
                   days_plus=0
                   text="Добро пожаловать, воспользуйтесь клавиатурой"
                   kb_m=keyboard
                   if event.user_id in level4:
                       level4.remove(event.user_id)
                       Ids_mass.pop(level4.index(event.user_id))
                   if event.user_id in level3:
                       level3.remove(event.user_id)
                   if event.user_id in level2:
                       days_mass.pop(level2.index(event.user_id))
                       level2.remove(event.user_id)
                       
                       #четвертый уровень################################################## add info
                elif event.user_id in level4:
                    asdasd=vk.users.get(user_id=event.user_id)
                    name_user=asdasd[0]['first_name']+'  '+asdasd[0]['last_name']
                    text=('Вы,  '+name_user + ", успешно забронировали и можете посмотреть на это в календаре https://calendar.google.com/calendar/b/1?cid=aHRib29raW5nZWtiQGdtYWlsLmNvbQ  "  )
                    booking_by_eventId(Ids_mass[level4.index(event.user_id)],name_user,event.text)
                    Ids_mass.pop(level4.index(event.user_id))
                    level4.remove(event.user_id)
                    kb_m=keyboard
                #третий уровень####################################################################time choose
                elif event.user_id in level3:

                    if event.text== 'К выбору даты':#### на пред. уровень
                        level3.remove(event.user_id)
                        level2.append(event.user_id)
                        days_mass.append(0)

                        text="Когда хотите посетить ХайТек цех ?"
                        date_1=datetime.datetime.today()
                        d1=(date_1-datetime.timedelta(hours=(datetime.datetime.now().hour)))
                        d2=(d1+datetime.timedelta(days=1))
                        d3=(d1+datetime.timedelta(days=2))
                        d4=(d1+datetime.timedelta(days=3))
  
                        kb_m=get_date_buttons(d1,d2,d3,d4)
                    else:
                        
                        if event.text==time_format(ids[1][0]):
                            Ids_mass.append(ids[0][0]) 
                        elif event.text==time_format(ids[1][1]):
                            Ids_mass.append(ids[0][1]) 
                        elif event.text==time_format(ids[1][2]):
                            Ids_mass.append(ids[0][2]) 
                        elif event.text==time_format(ids[1][3]):
                            Ids_mass.append(ids[0][3]) 
                        elif event.text==time_format(ids[1][4]):
                            Ids_mass.append(ids[0][4]) 
                            
                        
                        level3.remove(event.user_id)
                        level4.append(event.user_id)
                      
                        text="Какое оборудование и материалы будут необходимы?"
                        kb_m=keyboard_2
                      #второй уровень     
                elif event.user_id in level2:
                   
                    ##обрабатываем дату
                    
               ############################################################выбор даты№№№№№№№№№№№№№№№№№№№№№№№№
                    if event.text==d1.strftime("%d-%m-%Y") or event.text==d2.strftime("%d-%m-%Y") or event.text==d3.strftime("%d-%m-%Y") or event.text==d4.strftime("%d-%m-%Y"):
                        #print("trigger 1")
                        if event.text==d1.strftime("%d-%m-%Y"):
                            ids=id_events_call(d1)
                      
                        elif event.text==d2.strftime("%d-%m-%Y"):
                            ids=id_events_call(d2)
                        
                        elif event.text==d3.strftime("%d-%m-%Y"):
                            ids=id_events_call(d3)
                          
                        else:
                            ids=id_events_call(d4)
                    
                                    
                        
                        
                        

                        
                    
                        if ids[1][0]=='zero':
                           
                            text='В этот день Hi-tech цех уже занят, выберете другую дату'

                        
                        elif ids[1][1]=='zero':
                            kb_m=get_time_buttons(time_format(ids[1][0]),'zero','zero','zero','zero')
                            text='Одно свободное окно на выбранную дату'
                            if event.user_id in level2:
                                days_mass.pop(level2.index(event.user_id))
                                level2.remove(event.user_id)
                            if event.user_id not in level3:
                                level3.append(event.user_id)
                                
                        elif ids[1][2]=='zero':
                            kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),'zero','zero','zero')
                            text='Два свободных окна на выбранную дату, выберете время'
                            if event.user_id in level2:
                                days_mass.pop(level2.index(event.user_id))
                                level2.remove(event.user_id)
                            if event.user_id not in level3:
                                level3.append(event.user_id)
                        elif ids[1][3]=='zero':
                            kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][2]),'zero','zero')
                            text='Три свободных окна на выбранную дату, выберете время'
                            if event.user_id in level2:
                                days_mass.pop(level2.index(event.user_id))
                                level2.remove(event.user_id)
                            if event.user_id not in level3:
                                level3.append(event.user_id)
                        elif ids[1][4]=='zero':
                            kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][2]),time_format(ids[1][3]),'zero')
                            text='Четыре свободных окна на выбранную дату, выберете время'
                            if event.user_id in level2:
                                days_mass.pop(level2.index(event.user_id))
                                level2.remove(event.user_id)
                            if event.user_id not in level3:
                                level3.append(event.user_id)
                        elif ids[1][5]=='zero':
                            kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][2]),time_format(ids[1][3]),time_format(ids[1][4]))
                            text='Пять свободных окон на выбранную дату, выберете время'
                            if event.user_id in level2:
                                days_mass.pop(level2.index(event.user_id))
                                level2.remove(event.user_id)
                            if event.user_id not in level3:
                                level3.append(event.user_id)
                             #kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][1]),time_format(ids[1][1])) ######Вот здесь надо поработать, создание кнопок времени и тд
                        #else:
                            #kb_m=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][2]),time_format(ids[1][3]))
                           # text='Весь день свободен'
                        #else:
                           # print("else works")
                           # if event.user_id in level2:
                            #    days_mass.pop(level2.index(event.user_id))
                            #    level2.remove(event.user_id)
                           # if event.user_id not in level3:
                            #    level3.append(event.user_id)
                                
                                
                        
                    elif event.text==text_button22: #след неделя
                        
                        days_mass[level2.index(event.user_id)]=days_mass[level2.index(event.user_id)]+4
                        #days_mass.append(0)
                        
                        days_plus=days_mass[level2.index(event.user_id)]
                        date_1=datetime.datetime.today()+datetime.timedelta(days=days_plus)
                        d1=date_1-datetime.timedelta(hours=(datetime.datetime.now().hour))
                        d2=(d1+datetime.timedelta(days=1))
                   
                        d3=(d1+datetime.timedelta(days=2))
                        d4=(d1+datetime.timedelta(days=3))
                       # print('secind date')
                       #print(days_plus)
                        kb_m=get_date_buttons(d1,d2,d3,d4)

                        
                #########################################################################################################################################
                 #если юзер нажал на бронь
                elif event.text in booking_asso and event.user_id not in level2: 
                    text="Когда хотите посетить Hi-tech цех?"
                    date_1=datetime.datetime.today()
                    d1=(date_1-datetime.timedelta(hours=(datetime.datetime.now().hour)))
                    d2=(d1+datetime.timedelta(days=1))
                    d3=(d1+datetime.timedelta(days=2))
                    d4=(d1+datetime.timedelta(days=3))
                   # print('first date')

                    kb_m=get_date_buttons(d1,d2,d3,d4)
                    if event.user_id not in level2:
                        level2.append(event.user_id)
                        days_mass.append(0)

                   # print(str(level2.index(event.user_id))+'     номер юзера')
            #если юзер нажал привет                                                  
                elif event.text in hello_asso and event.user_id not in level2:
                    text="Привет"
            #если юзер нажал на погоду    
                elif event.text in weather_asso and event.user_id not in level2:
                    text=Weather.get_weather_today()
                elif event.user_id  in level2:
                       text="мне нужна дата"
                else:
                    text="Воспользуйтесь клавиатурой"
                    kb_m=keyboard
                    
                ##vk.messages.send(user_id=event.user_id,random_id=get_random_id(),keyboard=get_time_buttons(time_format(ids[1][0]),time_format(ids[1][1]),time_format(ids[1][1]),time_format(ids[1][1])).get_keyboard(),message=text)
                if kb_m==keyboard_2:
                    vk.messages.send(user_id=event.user_id,random_id=get_random_id(),message=text)
                else:
                    vk.messages.send(user_id=event.user_id,random_id=get_random_id(),keyboard=kb_m.get_keyboard(),message=text)    
   # except:
       # print ("error")
       # vk.messages.send(user_id=event.user_id,random_id=get_random_id(),keyboard=keyboard.get_keyboard(),message="перезагружаюсь")
       
    
while True:
    try:
        print('Работаю')
        main()
    except:
        print('Ошибка, перезапускаюсь')
        continue

#delta=datetime.datetime.today()-datetime.date.today()
#print(delta)
input("press anykey")
#main()

#booking_by_eventId(dates[0],'user takoy to','нужно больше золота')
