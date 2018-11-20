#coding:utf-8

'''Created by Ethan'''
import DisplayMenubar
import ControlEmail
import ParseEngineVPD
import os
import datetime
#import time
from ParseINIfile import ParseINIfile

data_number = int(cfg['HistoryTimes']['EngineTimes'])

Alarm_trigger = 0
ABTS_trigger = 0
ABTS_signal = 0
signal = 0
ABTS_lis = []
Time_number = []
errIP_lis = [[],[]]
tracepath = './HistoryFile/'
ABTS_filename = 'ABTS.doc'


'''
if os.name == 'nt':
    tracepath = tracepath.replace('/','\\')
    ABTS_tracepath = ABTS_filename.replace('/','\\')
 '''
  

class Alarm():
    def __init__(self):
        self.Restart_Alarm()
        self.ABTS_Alarm()
        self.errIP()

    def ABTS_Alarm(self): 
        global ABTS_trigger
        ABTS_trigger = 0
        for i in range(engine_number):
            if not engine_info[i]['ABTS and queue_full']:
                print 'Failed to get ABTS_data'
            else:
                self.ABTS_accumulative(i)
                self.ABTS_info(i)
                self.ABTS_initial(i)               
        self.File_decide()
        
    def ABTS_accumulative(self,i):      
        ABTS_alarm = 0 
        global ABTS_trigger
        global errIP_lis
        E_IP = engine_info[i]['IPaddress']
        E_IP_lis = E_IP.split('/')
        ABTS_values = engine_info[i]['ABTS and queue_full'].values()
        for ABTS_value in ABTS_values:
            for ABTS_value_a in ABTS_value:
                if ABTS_value_a == 0:
                    ABTS_alarm = ABTS_alarm + ABTS_value_a
        if ABTS_alarm > ABTS_signal:
            ABTS_trigger = 1
            errIP_lis[0].append(E_IP_lis[0])
          
    def ABTS_info(self,i):
        info_lis = []
        E_IP =  str(engine_info[i]["IPaddress"])
        if E_IP != '' : info_lis.append(E_IP)
        E_Uptime = str(engine_info[i]["Uptime"])
        if E_Uptime != '' : info_lis.append(E_Uptime)
        E_ABTS_values = engine_info[i]["ABTS and queue_full"].values()
        for E_ABTS_value in E_ABTS_values:
            for E_ABTS_each in E_ABTS_value:
                if E_ABTS_each != '' : info_lis.append(str(E_ABTS_each))
        
        for a in info_lis:
            ABTS_lis.append(a)
        self.list_initial(info_lis)
               
    def list_initial(self,lis_initial):
        while len(lis_initial) != 0:
            del lis_initial[0]
    
    def ABTS_initial(self,i):
        for ABTS_key in engine_info[i]['ABTS and queue_full']:
            self.list_initial(engine_info[i]['ABTS and queue_full'][ABTS_key])
            engine_info[i]['ABTS and queue_full'][ABTS_key] = [0,0]
            
    def File_decide(self):
        #if ABTS_trigger == 1  or Alarm_trigger==1 :            
        ABTS_a = ABTS_lis[:]
        File_trigger = 0
        for a in ABTS_a:
            if str(a).find('/') != -1 : ABTS_a.remove(a)
        for a in ABTS_a:
            if str(a).find(':') != -1 : ABTS_a.remove(a)
        for a in ABTS_a:
            if a != '0' : 
                File_trigger = 1
                break
        if File_trigger == 1 or Alarm_trigger == 1:self.Fileinitial(ABTS_lis)
        self.list_initial(ABTS_lis)
                                   
    def Fileinitial(self,Write_information):  
        TimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-7]
        fromname = ['Engine_IP','Uptime','ABTS_A1','Qfull_A1','ABTS_A2','Qfull_A2','ABTS_B1','Qfull_B1','ABTS_B2','Qfull_B2']
        q = 0
        for unitname in fromname:
            w = len(unitname)
            if w > q : q = w
        if (q % 2) != 0 : q=q+1           
        info_number = len(fromname)            
        if not os.path.exists(tracepath):
            os.makedirs(tracepath)
        with open(os.path.join(tracepath+ABTS_filename),'a+') as a:
            a.write('Time:' + TimeNow + '\n')
            for z in range(info_number):
                if z == 0 : a.write(fromname[z].center(24))
                elif z == 1 : a.write(fromname[z].center(14))
                else : a.write(fromname[z].center(q))
            a.write('\n')
            for j in range(0,len(Write_information),info_number):
                for z in range(len(Write_information[j:j+info_number])): 
                    if z == 0 : a.write(str(Write_information[j:j+info_number][z]).center(24))
                    elif z == 1 : a.write(str(Write_information[j:j+info_number][z]).center(14))
                    else : a.write(str(Write_information[j:j+info_number][z]).center(q))
                a.write('\n')
            a.write('\n')   
        with open(os.path.join(tracepath+ABTS_filename),'r') as r:
            lines = r.readlines()
        lines_length = len(lines)
        for line_id in range(lines_length):
            if lines[line_id].startswith('Time:'):
                Time_number.append(line_id)
        if len(Time_number) > data_number:
            with open(os.path.join(tracepath+ABTS_filename),'w') as w:
                for line in lines[Time_number[1]:]:
                    w.write(str(line))
        self.list_initial(Time_number)

        with open(os.path.join(tracepath+ABTS_filename),'r') as f:
            values = f.readlines()
        with open('./static/HCfile/ABTS.txt','w') as g:
            for value in values:
                g.write(value)

    def errIP(self):
        if errIP_lis[0] or errIP_lis[1]:
            self.list_initial(ErrList['Queue full&ABTS Error'])
            ErrList['Queue full&ABTS Error'] = errIP_lis[0][:]
            self.list_initial(ErrList['EngineReboot'])
            ErrList['EngineReboot'] = errIP_lis[1][:]            
            self.list_initial(errIP_lis[0])
            self.list_initial(errIP_lis[1])                
        
    def Restart_Alarm(self):
        global Alarm_trigger
        Alarm_trigger = 0
        for eng_id in range(engine_number):
            E_IP_lis = engine_info[eng_id]['IPaddress'].split('/')                
            a = engine_info[eng_id]['Uptime'].split(':') 
            if a[0] == ' 00' and int(a[-2]) < 30:
                Alarm_trigger = 1
                errIP_lis[1].append(E_IP_lis[0])

             
