#coding:utf-8
import DisplayMenubar
import ControlEmail
import ParseEngineVPD
import SWPortErrorAnalyze
import os
import EngineAnalyze

status=[]
class Alarm():
    def  __init__(self):
        Engine_trigger=EngineAnalyze.Alarm_trigger
        SWPortErrorAnalyze.SwitchAlarm()
        Switch_trigger = SWPortErrorAnalyze.Ecount_trigger
        ABTS_trigger=EngineAnalyze.ABTS_trigger

        if ABTS_trigger==1 or Switch_trigger==1 or Engine_trigger==1:
            SIGNAL[0]= 1
            del status[:]
            del ErrList['SwitchError'][:]
            SWPortErrorAnalyze.SwitchAlarm()
            self.SanAllGood(Engine_trigger,Switch_trigger,ABTS_trigger)
        self.SendEmail(status)

    def SanAllGood(self,a,b,c):
        global status
        if a == 1:
            status.append('Engine Reboot')
        if b == 1:
            status.append('Switch error')
            SWPortErrorAnalyze.ClearPortError()
        if c == 1:
            status.append('Queue full&ABTS Error')
        
    def __SendEmailNotification(self, status = 'Unknow'):
        if cfg['General']['EMAIL_NOTIFICATION'][1:-1] == "ENABLED":
            p = DisplayMenubar.DisplayMenubar()
            p.GetEmailInfo()
            t = ControlEmail.xEmail()
            t.auto_send_message(email_info,status)

    def SendEmail(self,status):
        if SIGNAL[0]==1:
            self.__SendEmailNotification(status)
