#!/usr/bin/python
# coding: utf8
"""
Control Email Module

Created by Susan Cheng on 2015-04-11.
Copyright (c) 2015-2016 __Loxoll__. All rights reserved.
"""
#

import os, sys, time, glob
import zipfile
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import base64
import shutil
import tkMessageBox
import datetime
import DisplayMenubar
import SWPortErrorAnalyze
from SendAlarmEmail import Alarm

file_name = os.path.basename(__file__)

#
# Telnet executive class, service all TCP related requests
#
class xEmail(object):

    def __init__(self):
        dbg.printDBG1(file_name, "initiate xEmail")
        pass
        
    def send_message(self, info):
        
        uu = info["uu"]
        ww = info["ww"]

        FROM = info["uu"]
        TO = [info["recipient1"], info["recipient2"], info["recipient3"], info["recipient4"], info["recipient5"], ]  # must be a list
        TO =[recipent for recipent in TO if recipent.replace(" ","")] 
        
        

        s = cfg['General']['LOCATION'][1:-1]
        SUBJECT = "Location: "+s+"; "+info["subject"] 

        s = cfg['Engine0']['IP']
        TEXT = info["message"] + "\n" + \
                "Engine IP = " + s
       
        # Prepare actual message   """\From: %s\nTo: %s\nSubject: %s\n\n%s     
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s     
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        ans = tkMessageBox.askokcancel("Send Email", 
            "The following test Message will be sent out :\r\r%s" % message[1:])

        
        if ans != True:
            tkMessageBox.showinfo("Send Email", "Action has been cancelled.")
            return False

        try:
            if smtp_ssl == "Yes":
                server = smtplib.SMTP_SSL(info["server"], info["port"])
               
            else:
                smtp_host = info["server"]
                smtp_port = info["port"]
                server = smtplib.SMTP()
                print 'server:',server
        except:
            dbg.printDBG1(file_name, "Failed to access smtp server!")
            tkMessageBox.showerror("Send Email", "Not able to access the smtp server") 
            return False
        try:
            if smtp_ssl != "Yes":
                server.connect(smtp_host,smtp_port)
#                server.settimeout(10)
                server.ehlo()
                server.starttls()
            server.login(uu,ww)
            
        except:
            print 'cannot connect...'
            dbg.printDBG1(file_name, "Wrong ID or PW")
            tkMessageBox.showerror("Send Email", "Wrong ID or PW!")
            return False
        try:    
            server.sendmail(FROM, TO,message)       

        except:
            dbg.printDBG1(file_name, "Failed to sent email")
            tkMessageBox.showerror("Send Email", "Not able to send email!")
            return False

        server.close()
        dbg.printDBG1(file_name, "Successfully sent email")
        
        return True
#
    def auto_send_message(self, info, status):
        time_now = datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S.%f')
        print "...attempt to send warning Email at %s" % time_now
        
        uu = info["uu"]
        ww = info["ww"]
        
        FROM = info["uu"]
        TO = [info["recipient1"], info["recipient2"], info["recipient3"], info["recipient4"], info["recipient5"], ]  # must be a list
        TO =[recipent for recipent in TO if recipent.replace(" ","")] 

        s = cfg['General']['LOCATION'][1:-1]
        SUBJECT = "Location: "+s+"; "+info["subject"] + "; status: %s" % status

        s = cfg['Engine0']['IP']
        TEXT = info["message"] + "\n" + \
                "Engine IP = " + s
        try:
            if 'Switch error' in status and 'Queue full&ABTS Error' in status and 'Engine Reboot' in status  :
                s='Reboot Engine IP is :'+ str(ErrList['EngineReboot'])+'\n'+\
                    'Queue full&ABTS Error Engine IP is :'+ str(ErrList['Queue full&ABTS Error'])+'\n'+\
                        'Error Switch IP is :'+str(ErrList['SwitchError'])
                TEXT = info["message"] + "\n" + s

            elif 'Engine Reboot' in status and 'Switch error' in status  :
                s='Reboot Engine IP is :'+str(ErrList['EngineReboot'])+'\n'+\
                    'Error Switch IP is :'+str(ErrList['SwitchError'])
                TEXT = info["message"] + "\n" + s
            
            elif 'Switch error'in status and 'Queue full&ABTS Error' in status:
                s='Queue full&ABTS Error Engine IP is :'+str(ErrList['Queue full&ABTS Error'])+'\n'+\
                    'Error Switch IP is :'+str(ErrList['SwitchError'])
                TEXT = info["message"] + "\n" + s

            elif 'Engine Reboot' in status and 'Queue full&ABTS Error' in status:
                s='Reboot Engine IP is :'+str(ErrList['EngineReboot'])+'\n'+\
                    'Queue full&ABTS Error Engine IP is :'+str(ErrList['Queue full&ABTS Error'])
                TEXT = info["message"] + "\n" + s

            elif 'Engine Reboot' in status:
                s = str(ErrList['EngineReboot'])
                TEXT = info["message"] + "\n" + \
                                "Reboot Engine IP = " + s

            elif 'Switch error' in status:
                s = str(ErrList['SwitchError'])
                TEXT = info["message"] + "\n" + \
                            "Error Switch IP = " + s

            elif 'Queue full&ABTS Error' in status:
                s = str(ErrList['Queue full&ABTS Error'])
                TEXT = info["message"] + "\n" + \
                            "Queue full&ABTS Error Engine IP = " + s

            else:
                s = cfg['Engine0']['IP']
                TEXT = info["message"] + "\n" + \
                            "Engine IP = " + s

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        except:
            print 'send Email break' 
        
        
        try:
            if smtp_ssl == "Yes":
                server = smtplib.SMTP_SSL(info["server"], info["port"])
            else:
                smtp_host = info["server"]
                smtp_port = info["port"]
                server = smtplib.SMTP()
        except:
            dbg.printDBG1(file_name, "Failed to access smtp server!")
            return False
        try:            
            if smtp_ssl != "Yes":
                server.connect(smtp_host,smtp_port)
                server.ehlo()
                server.starttls()
            server.login(uu,ww)
        except:
            dbg.printDBG1(file_name, "Wrong ID or PW!")
            return False
        try:            
            server.sendmail(FROM, TO, message)
        except:
            dbg.printDBG1(file_name, "Failed to sent email")
            return False

        server.close()
        dbg.printDBG1(file_name, "Successfully sent email")
        return True
#
#
    def send_zipped_file(self, info, newest_file, file_to_send):
        uu = info["uu"]
        ww = info["ww"]
        FROM = info["uu"]
        
        es = cfg['General']['MAILTO']
        if es[1:-1] != "":
            TO = [es[1:-1]]
        
        s = cfg['General']['LOCATION'][1:-1]
        SUBJECT = "Diagnostic trace from location: "+ s

        msg_str = " "
        for i in range (engine_number):
            if current_engine[i][0] == 'off': continue
            msg_str = msg_str + cfg['Engine%s' % i]['IP'] + " "
            
        TEXT = info["message"] + "\n" + \
                "Involved Engine IPs: " + msg_str + "\n\n"
        
        # Prepare actual message
#        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
#        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#
        msg = MIMEMultipart()
        msg["From"] = FROM
        msg["To"] = ','.join(TO)
        msg["Subject"] = SUBJECT
        text_part = MIMEText(TEXT, 'plain')
#
        shutil.copyfile(newest_file, file_to_send)
        fp = open(file_to_send, "rb") # open as binary file
        attachment = MIMEBase('application', "octet-stream")
        attachment.set_payload(fp.read())
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=file_to_send)
#
        msg.attach(text_part)
        msg.attach(attachment)
        fp.close()  
        os.remove(file_to_send)
        
        try:
            if smtp_ssl == "Yes":
                server = smtplib.SMTP_SSL(info["server"], info["port"])
            else:
                smtp_host = info["server"]
                smtp_port = info["port"]
                server = smtplib.SMTP()
        except:
            dbg.printDBG1(file_name, "Failed to access smtp server!")
            return False
        try:            
            if smtp_ssl != "Yes":
                server.connect(smtp_host,smtp_port)
                server.ehlo()
                server.starttls()
            server.login(uu,ww)
        except:
            dbg.printDBG1(file_name, "Wrong ID or PW!")
            return False
        try:            
            server.sendmail(FROM, TO, msg.as_string())
        except:
            dbg.printDBG1(file_name, "Failed to sent zipped file through email")
            return False

        server.close()
        dbg.printDBG1(file_name, "Successfully sent zipped file through email")
        return True

if __name__ == '__main__':    
    sys.exit()

