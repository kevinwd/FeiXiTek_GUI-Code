# coding:utf-8
from datetime import timedelta

from flask import Flask, render_template, request, json,make_response
import os
import SWPortErrorAnalyze
Switch_number=SWPortErrorAnalyze.Switch_number
Switch_Portnum=SWPortErrorAnalyze.Switch_Portnum
app = Flask(__name__)  # 创建应用对象

#app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)

def check_mirror_status(engine):
    fail = [1]  # fail signal 
    ml_fail = ""  # fail message
    mlun_member_idx = [3, 5, 7, 9]  # mirror members' index list

    for mlun in engine_info[engine]['Mirror'].keys():
        fail[0] = 0
        ml_fail += mlun + ": "
        for k in mlun_member_idx:
            if engine_info[engine]['Mirror'][mlun][k + 1] not in ("OK", "-"):
                fail[0] = 1
                ml_fail.append(engine_info[engine]['Mirror'][mlun][k] + "-")
                ml_fail.append(engine_info[engine]['Mirror'][mlun][k + 1] + " ")
    
    if fail[0] == 0:
        return "All OK"
    else:
        return ml_fail



@app.route('/switch/')
def SwitchFile():
    return render_template("switch.html")


@app.route('/engine/')
def EngineFile():
    return render_template("engine.html")


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        username = request.values.get('button_name')
        if username == '1':
            SIGNAL[0]= 0
            del ErrList['EngineReboot'][:]
            del ErrList['Queue full&ABTS Error'][:]
            del ErrList['SwitchError'][:]

# engine数据
    engine_list = []
    uptime_list = [] 
    status_list = []
    alert_list = []
    master_list = []
    mirror_list = []
    
    #print "engine #:", engine_number
    for i in range(engine_number):
        engine_list.append(engine_info[i]["IPaddress"])
        status_list.append(engine_info[i]["Status"])
        uptime_list.append(engine_info[i]["Uptime"])
        alert_list.append(engine_info[i]["Alert"])
        master_list.append(engine_info[i]["Master"])
        mirror_list.append(check_mirror_status(i)) 
    
# 交换机数据 
    SwitchIP_list = []
    SwitchIP_list2 = []
    Switch_Port_list = []
    Switch_Port_list2 = []
    frameTx_list = []
    frameRx_list = []
    encout_list = []
    discc3_list = []
    linkFL_list = []
    lossSC_list = []
    lossSG_list = []
    

    
    for i in range(len(Switch_info)):
        for port in sorted(Switch_info[i]["PortInfo"].keys()):
            SwitchIP_list.append(Switch_info[i]["SwitchIP"])
            Switch_Port_list.append(port)
            frameTx_list.append(Switch_info[i]["PortInfo"][port][0]["FrameTx"])
            frameRx_list.append(Switch_info[i]["PortInfo"][port][1]["FrameRx"])
            encout_list.append(Switch_info[i]["PortInfo"][port][2]["Encout"])
            discc3_list.append(Switch_info[i]["PortInfo"][port][3]["Discc3"])
            linkFL_list.append(Switch_info[i]["PortInfo"][port][4]["LinkFL"])
            lossSC_list.append(Switch_info[i]["PortInfo"][port][5]["LossSC"])
            lossSG_list.append(Switch_info[i]["PortInfo"][port][6]["LossSG"])
    
#即时错误信息的获取
    ErrList_list = ""
    QFAE_list = ""
    SE_list = ""
    for i in ErrList['EngineReboot']:
         ErrList_list += i+ " | "
    for i in ErrList['Queue full&ABTS Error']:
         QFAE_list += i+ " | "
         
    for i in ErrList['SwitchError']:
         SE_list += i+ " | "     
    



    context = {
#         engine
        'engine_number':engine_number,
        'engine_list':engine_list,
        'status_list':status_list,
        'uptime_list':uptime_list,
        'alert_list':alert_list,
        'master_list' : master_list,
        'Mirror_list':mirror_list,
        "signal":SIGNAL[0],

#         交换机
        
        "SwitchIP_list2" :SwitchIP_list,
        "Switch_Port_list2":Switch_Port_list,
        "Switch_Portnum":Switch_Portnum,
        "Switch_number":Switch_number,
        "frameTx_list":frameTx_list,
        "frameRx_list":frameRx_list,
        "encout_list":encout_list,
        "discc3_list":discc3_list,
        "linkFL_list":linkFL_list,
        "lossSC_list":lossSC_list,
        "lossSG_list":lossSG_list,

#即时错误信息

        "ErrList_list":ErrList_list,
        "QFAE_list":QFAE_list,
        "SE_list":SE_list,
        }
    return render_template("index.html", **context
                           )   
#关闭Flask服务器的方法
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

#关闭Flask服务器的函数，对应网页地址:/shutdown
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'The flask server shuts down.'

def main():    
    app.run(port=3333)

