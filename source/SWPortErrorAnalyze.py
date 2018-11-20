#-*- coding:utf-8 -*-
import os
import time
import shutil
import codecs
import re
import sys
import collections
from collections import OrderedDict
import paramiko

class SSHConnection(object):       #connect to FCswitch
    def __init__(self, host, port, username, password, timeout):
        self._host = host
        self._port = port
        self._timeout = timeout
        self._username = username
        self._password = password
        self._client = None
        self._sftp = None
        self._connect()

    def _connect(self):
        try:
            objSSHClient = paramiko.SSHClient()
            objSSHClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            objSSHClient.connect(self._host, port=self._port,
                                 username=self._username,
                                 password=self._password,
                                 timeout=self._timeout)
            self._client = objSSHClient
            #self._sftp = objSSHClient.open_sftp() #can not open
        except Exception as E:
            print('Connect to {} Fail in {} Seconds ...'.format(self._host, self._timeout))

    def download(self, remotepath, localpath):
        self._sftp.get(remotepath, localpath)

    def upload(self, localpath, remotepath):
        self._sftp.put(localpath, remotepath)

    def exec_command(self, command):
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            # print(data.strip())
            return data
        err = stderr.read()
        if len(err) > 0:
            #print(err.strip())
            return err

    def close(self):
        if self._client:
            self._client.close()

Ecount_trigger = 0
strSWUserName =cfg['SWSetting']['username']
strSWPasswd = cfg['SWSetting']['password']
SwitchName = cfg['SWSetting']['switchname']
Switch_times=cfg['HistoryTimes']['SwitchTimes']
lstSANSwitchIPs = []
lstSWPorts=[]
for ii in cfg['SWPorts']:
    ii=str(ii)
    lstSANSwitchIPs.append(ii)
for key,value in cfg['SWPorts'].items():
    lstSWPorts.append(value)
Switch_number=len(lstSANSwitchIPs)
Switch_Portnum=0
oddSWPort = collections.OrderedDict()
for i in lstSWPorts:
    i=eval(i)
    for portnu in i:
        Switch_Portnum=Switch_Portnum+1
for indexSwIP in range(len(lstSANSwitchIPs)):
    lstSWPorts[indexSwIP] = eval(lstSWPorts[indexSwIP])
    for intPortNum in lstSWPorts[indexSwIP]:
        pass

def boolPortinLine(intPort, strLine):
    lstLine = strLine.split()
    if (str(intPort) + ':') in lstLine:
        return True
    else:
        return False

err_ls=[]
def findDataAndErr(intPortNum, lstPortErrLines):      #pick Switch info according port number
    for portErrLine in lstPortErrLines:
        if boolPortinLine(intPortNum, portErrLine) == True:
            reDataAndErr = re.compile(r'(.*:)((\s+\S+){2})((\s+\S+){6})((\s+\S+){5})(.*)')
            resultDataAndErr = reDataAndErr.match(portErrLine)
            return(resultDataAndErr.group(2).split() + resultDataAndErr.group(6).split()) #save 7 data
    

def initSwitchInfo(i):          #init Switch_info 
    Switch_info[i]['SwitchIP'] = {}
    Switch_info[i]['Link_time'] = {}
    Switch_info[i]['PortInfo'] = {}

port=22
connect_time=5
def SWPortErrorAnalyze():  #Switch_info function
    err_ls=[]    
    tracepath = './trace/'
        #if not os.path.exists(tracepath): os.makedirs(self.tracepath)
    for indexSwIP in range(len(lstSANSwitchIPs)):
        strPortErrorFileName = 'SW_porterrshow_{}.log'.format(
            lstSANSwitchIPs[indexSwIP])
        strPortErrorFileName=os.path.join(tracepath,strPortErrorFileName)
        objFilePorterrshow = open(strPortErrorFileName, 'w')
        try:      #connect to FCswitch
            if SwitchName=='"brocade"':
                ss=SSHConnection(lstSANSwitchIPs[indexSwIP], port, strSWUserName, strSWPasswd,connect_time)
                Date_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())  
                objFilePorterrshow.write('Date:'+str(Date_now)+' '+'SwitchIP:'+str(lstSANSwitchIPs[indexSwIP])+'\n')
                objFilePorterrshow.write(str(ss.exec_command('porterrshow')))
                objFilePorterrshow.close()
                ss.close()
        except Exception as E:
            print('Connect to SAN Switch {} Failed ...'.format(lstSANSwitchIPs[indexSwIP]))
            break
        if '3.6' in sys.version.split(' ')[0]:
            lstPortErrLines = codecs.open(strPortErrorFileName).readlines()
        elif '3.4' in sys.version.split(' ')[0]:
            lstPortErrLines = open(strPortErrorFileName).readlines()
        elif '2.7' in sys.version.split(' ')[0]:
            with open(strPortErrorFileName) as fff:
                lstPortErrLines = fff.readlines()
    
        #Switch_info assignment
        for intPortNum in lstSWPorts[indexSwIP]:
            #print 'num',str(num)+str(intPortNum) 
            lstErrInfo = findDataAndErr(intPortNum, lstPortErrLines)
            Switch_info[indexSwIP]['PortInfo'][intPortNum]= lstErrInfo
            F=['FrameTx','FrameRx','Encout','Discc3','LinkFL','LossSC','LossSG']        
            a=Switch_info[indexSwIP]['PortInfo'][intPortNum]  
            for i in range(7):
                a[i]=F[i]+':'+a[i]
                a[i]=a[i].split(':')
                a[i]={a[i][0] : a[i][1]}   
            Switch_info[indexSwIP]['SwitchIP']=lstSANSwitchIPs[indexSwIP]
            Date_now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            Switch_info[indexSwIP]['Link_time']=Date_now

def SwitchAlarm():      #Switch Ecount_trigger 
    err_ls=[]
    SwitcheIP=[]
    for indexSwIP in range(len(lstSANSwitchIPs)):
        for intPortNum in lstSWPorts[indexSwIP]:
                try:
                    Encout_list=Switch_info[indexSwIP]['PortInfo'][intPortNum][2]['Encout'] 
                    Discc3_list=Switch_info[indexSwIP]['PortInfo'][intPortNum][3]['Discc3']
                    err_ls.append(Encout_list)
                    err_ls.append(Discc3_list)

                    if int(Encout_list) != 0 or int(Discc3_list) != 0: #collect Switch error IP
                        Switch_eIP=Switch_info[indexSwIP]['SwitchIP']   
                        SwitcheIP.append(Switch_eIP)
                        ErrList['SwitchError'] = list(set(SwitcheIP))
                except:
                    #print 'break'
                    break

    global Ecount_trigger
    for encout_l in err_ls:
        if encout_l != '0':
            Ecount_trigger = 1
        else:
            Ecount_trigger = 0
        if Ecount_trigger == 0:
            for i in err_ls:
                if i != '0':
                    Ecount_trigger = 1      
    #return Ecount_trigger

def ClearPortError():       #ClearPortError according port number
    for indexSwIP in range(len(lstSANSwitchIPs)):
        try:
            ss=SSHConnection(lstSANSwitchIPs[indexSwIP], port, strSWUserName, strSWPasswd,connect_time)
            for strPortNum in lstSWPorts[indexSwIP]:
                ss.exec_command('statsclear {} '.format(str(strPortNum)))
            print 'clean errorcount successfully'
        except:
            print('Connect to SAN Switch {} Failed ...'.format(lstSANSwitchIPs[indexSwIP]))
            break
        ss.close()
        
count=0
def SaveSwInfo_hist():    #Save Switch error info 
    if Ecount_trigger==1: 
        tracepath = './trace'
        HistoryFile='./Historyfile'
        if not os.path.exists(HistoryFile): os.makedirs(HistoryFile)
        SwitchinfoFile='Switchinfo.doc'
        HisTracepath=os.path.join(HistoryFile,SwitchinfoFile)
        for indexSwIP in range(len(lstSANSwitchIPs)):
            h=open(HisTracepath,'a')
            h.write(str(Switch_info[indexSwIP]['Link_time'])+' '+str(Switch_info[indexSwIP]['SwitchIP'])+'\n')
            h.write('PortID'.center(8) + 'FramTX'.center(8) + 'FramRX'.center(8) + 'encout'.center(8) + 'Discc3'.center(8) + 'LinkFL'.center(8) + 'LossSC'.center(8) + 'LossSG' + '\n')
            for intPortNum in lstSWPorts[indexSwIP]:
                h.write(str(intPortNum).center(8))
                try:
                    aqq=Switch_info[indexSwIP]['PortInfo'][intPortNum]
                    PortInfo_values=[item[key] for item in aqq for key in item]  #all 7 data
                    for PortInfo_value in PortInfo_values:
                        h.write(PortInfo_value.center(8))
                    h.write('\n')
                except:
                    return False
            h.write('\n')
            h.close()

        g=open(HisTracepath,'r') #keep ten times Switch Error data
        global count
        count=len(g.readlines())
        g.close()
        Switch_line=int((Switch_Portnum+6)*int(Switch_times))
        Switch_l=int(Switch_Portnum+6)
        if count>=Switch_line: 
            j=open(HisTracepath,'r')
            rw_l=j.readlines()[Switch_l:Switch_line]
            k=open(HisTracepath,'w')
            for rw in rw_l:
                k.write(rw)
            k.close()
            j.close()
        if not os.path.exists('./static/HCfile/'): os.makedirs('./static/HCfile/')
        with open(HisTracepath,'r') as du:
            values = du.readlines()
        with open('./static/HCfile/Switchinfo.txt','w') as f:
            for value in values:
                f.write(value)
