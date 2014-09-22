# _*_ coding: UTF-8 _*_

__authors__ = ["Man Quanxing (manquanxing@gmail.com)"]
__version__ = "0.8.0"
__copyright__ = """
Copyright (c) 2011,2014, Mingvale Technology Co.,Ltd.
All rights reserved.
"""

import datetime
from twisted.internet import reactor
from twisted.python import log

import cherrypy
from twisted.web.wsgi import WSGIResource
from mako.template import Template

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

from www_table import WTable

icon_box = "M2,0h28c1.104,0,2,0.896,2,2v12c0,1.104-0.896,2-2,2H2c-1.104,0-2-0.896-2-2l0,0V2C0,0.896,0.896,0,2,0z"

icon_PM ="M7.361,3.676h4.173c0.825,0,1.491,0.233,1.998,0.701s0.761,1.124,0.761,1.971c0,0.728-0.227,1.361-0.679,1.901c-0.453,0.539-1.146,0.81-2.078,0.81H8.624V13H7.361V3.676z M12.26,4.957c-0.277-0.131-0.658-0.196-1.141-0.196H8.624v3.231h2.496c0.563,0,1.02-0.121,1.371-0.362c0.351-0.241,0.526-0.667,0.526-1.276C13.017,5.668,12.765,5.203,12.26,4.957z"
icon_PM += "M15.879,3.676h1.81l2.681,7.883l2.663-7.883h1.797V13h-1.207V7.496c0-0.189,0.005-0.505,0.014-0.945c0.008-0.44,0.012-0.912,0.012-1.416L20.986,13h-1.252l-2.687-7.865v0.286c0,0.229,0.006,0.576,0.019,1.044s0.019,0.812,0.019,1.031V13h-1.206V3.676z"


icon_LU ="M8.681,3.676h1.263v8.213h4.678V13H8.681V3.676z"
icon_LU += "M17.276,3.676v5.764c0,0.677,0.128,1.239,0.384,1.688c0.38,0.678,1.02,1.016,1.919,1.016c1.079,0,1.813-0.365,2.201-1.098c0.209-0.397,0.313-0.934,0.313-1.605V3.676h1.275v5.236c0,1.146-0.154,2.029-0.465,2.646c-0.568,1.126-1.643,1.689-3.223,1.689c-1.58,0-2.652-0.563-3.217-1.689C16.155,10.941,16,10.059,16,8.912V3.676H17.276z"

icon_TU = "M15.46,3.676v1.11h-3.142V13h-1.276V4.786H7.9v-1.11H15.46z"
icon_TU += "M17.987,3.676v5.764c0,0.677,0.128,1.239,0.384,1.688c0.379,0.678,1.02,1.016,1.919,1.016c1.079,0,1.813-0.365,2.201-1.098c0.209-0.397,0.313-0.934,0.313-1.605V3.676h1.275v5.236c0,1.146-0.154,2.029-0.465,2.646c-0.568,1.126-1.643,1.689-3.223,1.689s-2.652-0.563-3.217-1.689c-0.31-0.617-0.465-1.5-0.465-2.646V3.676H17.987z"

icon_RM="M7.393,3.676h4.239c0.698,0,1.273,0.104,1.727,0.311c0.86,0.397,1.29,1.132,1.29,2.203c0,0.559-0.115,1.016-0.346,1.371c-0.23,0.355-0.553,0.641-0.968,0.856c0.364,0.148,0.638,0.343,0.822,0.584c0.184,0.241,0.287,0.633,0.308,1.175l0.044,1.25c0.013,0.355,0.042,0.62,0.089,0.793c0.076,0.297,0.211,0.487,0.406,0.572V13h-1.549c-0.042-0.08-0.076-0.184-0.102-0.311s-0.046-0.373-0.063-0.736l-0.076-1.556c-0.029-0.609-0.249-1.018-0.66-1.226c-0.235-0.113-0.603-0.171-1.104-0.171H8.656V13H7.393V3.676z M11.495,7.947c0.576,0,1.032-0.118,1.368-0.355s0.503-0.664,0.503-1.282c0-0.664-0.234-1.117-0.704-1.358c-0.251-0.127-0.586-0.19-1.006-0.19h-3v3.187H11.495z"
icon_RM +="M16.597,3.676h1.81l2.682,7.883l2.662-7.883h1.797V13h-1.206V7.496c0-0.189,0.005-0.505,0.013-0.945s0.013-0.912,0.013-1.416L21.704,13h-1.252l-2.688-7.865v0.286c0,0.229,0.006,0.576,0.019,1.044s0.019,0.812,0.019,1.031V13h-1.206V3.676z"

import cgi
import tempfile

class myFieldStorage(cgi.FieldStorage):
    """Our version uses a named temporary file instead of the default
    non-named file; keeping it visibile (named), allows us to create a
    2nd link after the upload is done, thus avoiding the overhead of
    making a copy to the destination filename."""
    
    def make_file(self, binary=None):
        return tempfile.NamedTemporaryFile()


def noBodyProcess():
    """Sets cherrypy.request.process_request_body = False, giving
    us direct control of the file upload destination. By default
    cherrypy loads it to memory, we are directing it to disk."""
    cherrypy.request.process_request_body = False

cherrypy.tools.noBodyProcess = cherrypy.Tool('before_request_body', noBodyProcess)



# Our CherryPy application
class Root(object):

    alarm_tags = [('tag_1',u' [1] 入侵者'),
                  ('tag_2',u' [2] 动物'),
                  ('tag_3',u' [3] 天气'),
                  ('tag_4',u' [4] 工作人员'),
                  ('tag_5',u' [5] 植被'),
                  ('tag_6',u' [6] 维修'),
                  ('tag_7',u' [7] 试验'),
                  ('tag_8',u' [8] 垃圾'),
                  ('tag_9',u' [9] 未知事物')]

    relays = [('relay_1','relay_off',u' [1] 联动'),
              ('relay_2','relay_off',u' [2] 联动'),
              ('relay_3','relay_off',u' [3] 联动'),
              ('relay_4','relay_off',u' [4] 联动'),
              ('relay_5','relay_off',u' [5] 联动'),
              ('relay_6','relay_off',u' [6] 联动'),
              ('relay_7','relay_off',u' [7] 联动'),
              ('relay_8','relay_off',u' [8] 联动')]

    message_btns = [('left_btn',u'报警'),
                    ('mid_btn',u'选择'),
                    ('right_btn',u'控制')]

    segments = {
        'Seg_1': {'id': 1, 
                  'x0':638,   'y0': 563,    
                  'x1':980,   'y1': 720, 
                  'name' : u'南墙东段',
                  'secure' : 1,
                  'status': 0 },

        'Seg_2': {'id': 2, 
                  'x0':1104,  'y0': 589,    
                  'x1':980,   'y1': 720, 
                  'name' : u'东墙南段',
                  'secure' : 1,
                  'status': 0 },

        'Seg_3': {'id': 3, 
                  'x0':1418,  'y0': 259,    
                  'x1':1104,   'y1': 589, 
                  'name' : u'东墙北段',
                  'secure' : 1,
                  'status': 0 },


        'Seg_4': {'id': 4, 
                  'x0':1016,  'y0': 161,    
                  'x1':1418,  'y1': 259, 
                  'name' : u'北墙',
                  'secure' : 0,
                  'status': 0 },

        'Seg_5': {'id': 5,
                  'x0':780,   'y0': 296, 
                  'x1':1016,  'y1': 161, 
                  'name' : u'西墙北段',
                  'secure' : 1,
                  'status': 0 },

        'Seg_6': {'id': 6,
                  'x0':457,   'y0': 480, 
                  'x1':780,   'y1': 296,   
                  'name' : u'西墙南段',
                  'secure' : 0,
                  'status': 0 },

        'Seg_7': {'id': 7, 
                  'x0':567,   'y0': 533,    
                  'x1':457,   'y1': 480, 
                  'name' : u'南墙西段',
                  'secure' : 0,
                  'status': 0 },

    }

    auxiliaries = {
        'Aux_1': {'id': 1, 
                  'x0': 865,  'y0': 425,  
                  'x1': 803,  'y1': 402,
                  'x2': 804,  'y2': 431,
                  'x3': 866,  'y3': 454,  
                  'name': u'小门',
                  'secure' : 1,
                  'status': 0 },

        'Aux_2': {'id': 2, 
                  'x0': 629,   'y0': 590, 
                  'x1': 633,   'y1': 620, 
                  'x2': 571,   'y2': 588, 
                  'x3': 566,   'y3': 558, 
                  'name': u'大门',
                  'secure' : 1,
                  'status': 0 },
    }

    alarms = { }


    devices = {
        'Dev_1': {'id': 1,
                  'type': 'PM', 
                  'x0': 300,  'y0': 60,  
                  'x1': 380,  'y1': 88,
                  'name': u'PM1',
                  'secure' : 1,
                  'status': 0 },

        'Dev_2': {'id': 2, 
                  'type': 'LU', 
                  'x0': 130,  'y0': 100,  
                  'x1': 180,  'y1': 128,
                  'name': u'LU2',
                  'secure' : 0,
                  'status': 2 },

        'Dev_3': {'id': 3, 
                  'type': 'TU', 
                  'x0': 230,  'y0': 100,  
                  'x1': 280,  'y1': 128,
                  'name': u'TU3',
                  'secure' : 0,
                  'status': 1 },

        'Dev_4': {'id': 3, 
                  'type': 'RM', 
                  'x0': 330,  'y0': 100,  
                  'x1': 380,  'y1': 128,
                  'name': u'RM3',
                  'secure' : 0,
                  'status': 1 },
    }

    log_datas = {}
    log_ready = False

#    alarm_title = 'Alarm Logs'
#    alarm_heads = ['id','type','time_stamp','description','zone_id','zone_name','details','div']
    
    logs_title = u'GCM周界报警系统日志'
    logs_heads = [u'编号',u'发生时间',u'描述',u'详情',u'操作者',u'复位时间',u'事件标签',u'备注']
    

    def __init__(self, myRecords, alarm_logs = None,pm_line = None,gcm_io = None,wtable = None):
        self.logs_index = 0
        self.records = myRecords
        if self.records is None:
            log.msg("Need Alarm Log Database!")

        self.log_datas = {}
        self.log_ready = False

        self.alarm_logs = alarm_logs
        now_time = datetime.datetime.now()
        now_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        self._writeSystemRecord(info = u'GCM启动')

        self.pm_line = pm_line or None
        self.gcm_io =  gcm_io

        self.index_path = os.path.join(current_dir, 'data','static','index.html')
        self.temp_index = Template(filename=self.index_path)
    
        self.temp_path = os.path.join(current_dir, 'data','static','log_table.html')
        self.template = Template(filename=self.temp_path)

        self.setup_path = os.path.join(current_dir, 'data','static','setup.html')
        self.temp_setup = Template(filename=self.setup_path)
    

        self.www_table = wtable or None
        if self.www_table is not None:
            self.segments = self.www_table.getSegments() 
            self.auxiliaries = self.www_table.getAuxiliaries() 
            self.devices = self.www_table.getDevices()
            self.relays = self.www_table.getRelays()
            self.alarm_tags = self.www_table.getTags()

        self._updateDevices()
            

    def _updateDevices(self):
        for key in self.segments:
            dev = self.segments[key] 
            dev['path'] = ('M' + str(dev['x0']) + ',' + str(dev['y0']) + 
                           'L' + str(dev['x1']) + ',' + str(dev['y1']) )

            id_no = dev['id']
            secure = dev['secure']
            if secure == 1:
                status = 'Secure'
            else:
                status = 'Access'
            if self.pm_line is not None:
                self.pm_line.setDisplaySegmentStatus(dest=0,segment=id_no,status=status)
                
        for key in self.devices:
            dev = self.devices[key] 
            d_type = dev['type']
            id_no = dev['id']
            secure = dev['secure']
            if secure == 1:
                status = 'Secure'
            else:
                status = 'Access'
            if d_type == 'PM':
                dev['path'] = icon_box
                dev['fg'] = icon_PM
            elif d_type == 'LU':
                dev['path'] = icon_box 
                dev['fg'] = icon_LU
            elif d_type == 'TU':
                dev['path'] = icon_box 
                dev['fg'] = icon_TU
            elif d_type == 'RM':
                dev['path'] = icon_box
                dev['fg'] = icon_RM 

            if self.pm_line is not None:
                #log.msg("id_no=%r" % id_no)
                self.pm_line.secureTamper(dev_type = d_type, dest = id_no, status = status)
                
        for key in self.auxiliaries:
            dev = self.auxiliaries[key] 
            dev['path'] = ('M' + str(dev['x0']) + ',' + str(dev['y0']) + 
                           'L' + str(dev['x1']) + ',' + str(dev['y1']) +
                           'L' + str(dev['x2']) + ',' + str(dev['y2']) +
                           'L' + str(dev['x3']) + ',' + str(dev['y3']) + 'Z')

            aux = dev['name']
            secure = dev['secure']
            if secure == 1:
                status = 'Secure'
            else:
                status = 'Access'
            if self.pm_line is not None:
                self.pm_line.secureZone(zone_name=aux,status=status)
                #self.pm_line.securePmAuxiliary(dest=1,auxiliary=id_no,status=status)


    @cherrypy.expose
    def index(self):
        self.log_datas = {}
        self.log_ready = False

        main_page = self.temp_index.render(title='GCM', 
                                           tags = self.alarm_tags, 
                                           relays = self.relays,
                                           btns=self.message_btns)
        return main_page

    @cherrypy.expose
    def logs(self):
        #log.msg("The remote IP is %s" % cherrypy.request.remote.ip)
        log_table = self.template.render(title=self.logs_title, 
                                         heads = self.logs_heads, 
                                         rows = self.alarm_logs)
        return log_table


    def _writeSystemRecord(self,user='admin@127.0.0.1',info=''):
        now_time = datetime.datetime.now()
        now_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        rec = {'id': None,
               'occured': now_str,
               'description' : info,
               'details' : '',
               'operator': user,
               'disposition': '',
               'tag': '',
               'comment': ''}

        self.records.process_item(rec)
       
 


    def _writeAlarmRecord(self,key,alarm_tag,comment=''):
        log = self.alarms[key]
        now_time = datetime.datetime.now()
        now_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        rec = {'id': None,
               'occured': log['time'],
               'description' : log['name'],
               'details' : log['details'],
               'operator': 'user1@' + cherrypy.request.remote.ip,
               'disposition': now_str,
               'tag': self.alarm_tags[int(alarm_tag[4])-1][1],
               'comment': comment}

        self.records.process_item(rec)
        
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def resetAlarm(self,alarm_tag = None,alarm_id = None):
        if alarm_id in self.alarms:
            self._writeAlarmRecord(alarm_id,alarm_tag)
            del self.alarms[alarm_id];
        else:
            a_id = int(alarm_id)
            if a_id == -1:  # clear all alarms
                for key in self.alarms.keys():
                    self._writeAlarmRecord(key,alarm_tag,comment='???')
                    del self.alarms[key];
        return self.getNewestAlarm()


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getNewestAlarm(self,arg = None):
        n = len(self.alarm_logs)
        if n > 0: 
            for i in range(n):
                (a_id, a_type,time_stamp, name, z_id, z_name,details, div) = self.alarm_logs.pop() 
                if a_type == 'Cable Alarm':
                    xitem = 'ALM_' + ('%d' % a_id)
                    #seg = 'Seg_' + ('%d' % z_id)
                    seg = z_name
                    if seg in self.segments:
                        x0 = self.segments[seg]['x0']
                        x1 = self.segments[seg]['x1']
                        y0 = self.segments[seg]['y0']
                        y1 = self.segments[seg]['y1']

                        x = x1 * div + x0 * (1 - div)
                        y = y1 * div + y0 * (1 - div)
                        self.alarms[xitem] = { 'id'   : a_id,
                                               'type' : 0,
                                               'zone' : z_id,
                                               'time' : time_stamp,
                                               'x0'   : x,
                                               'y0'   : y,
                                               'name' : name,
                                               'details' : details,
                                               'status' : 0 }

                elif a_type == 'Auxiliary':
                    xitem = 'AUX_' + ('%d' % a_id)
                    aux =  z_name
                    if aux in self.auxiliaries:
                        x0 = self.auxiliaries[aux]['x0']
                        y0 = self.auxiliaries[aux]['y0']
                        x1 = self.auxiliaries[aux]['x1']
                        y1 = self.auxiliaries[aux]['y1']
                        x2 = self.auxiliaries[aux]['x2']
                        y2 = self.auxiliaries[aux]['y2']
                        x3 = self.auxiliaries[aux]['x3']
                        y3 = self.auxiliaries[aux]['y3']

                        self.alarms[xitem] = { 'id'   : a_id,
                                               'type' : 1,
                                               'zone' : z_id,
                                               'time' : time_stamp,
                                               'x0'   : x0,
                                               'y0'   : y0,
                                               'x1'   : x1,
                                               'y1'   : y1,
                                               'x2'   : x2,
                                               'y2'   : y2,
                                               'x3'   : x3,
                                               'y3'   : y3,
                                               'name' : name,
                                               'details' : details,
                                               'status' : 0 }

        
        message = self.alarms or {}
        return message

    def _updateRelayState(self):
        if self.gcm_io is not None:
            i = 0
            for (idx,status,nc) in self.relays:
                relay_state = self.gcm_io.get_relay_state(i+1)
                if(relay_state == 1):
                    status = 'relay_on'
                else:
                    status = 'relay_off'
                self.relays[i] = (idx,status,nc)
                i += 1
            
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getRelayStatus(self,relay=0,stat=0):

        self._updateRelayState()

        stat = int(stat)
        if relay != 0 :
            i = 0
            for (idx,status,nc) in self.relays:
                if relay == idx:
                    if stat == 0:
                        st = 'relay_off'
                        if self.gcm_io is not None:
                            self.gcm_io.set_relay_off(i+1)
                        self._writeSystemRecord(user = 'user1@' + cherrypy.request.remote.ip ,
                                                info = (u'关闭继电器[%d]'%(i+1)))
                    else:
                        st = 'relay_on'
                        if self.gcm_io is not None:
                            self.gcm_io.set_relay_on(i+1)
                        self._writeSystemRecord(user = 'user1@' + cherrypy.request.remote.ip,
                                                info = (u'打开继电器[%d]'%(i+1)))
                    self.relays[i] = (idx,st,nc)
                    break;
                i += 1
        message = {}
        for (idx,status,nc) in self.relays:
            if status == 'relay_on':
                st = 1
            else:
                st = 0
            message[idx] = st 
        log.msg("relays: %r" % self.relays)
        return message

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getDisplaySegment(self,seg_no):
        message = self.segments or {}
        return message

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def setDisplaySegmentStatus(self,seg_no,stat):
        d = self.segments
        seg = int(seg_no)
        st = int(stat)
        user = 'user1@' + cherrypy.request.remote.ip
        for key in d:
            val = d[key]
            if val['id'] == seg:
                if st == 0 or st == 1:
                    d[key]['secure'] = st
                    if st == 1:
                        status = 'Secure'
                        info = (u'布防显示段[%d]' % seg)
                    else:
                        status = 'Access'
                        info = (u'撤防显示段[%d]' % seg)
                    if self.pm_line is not None:
                        self.pm_line.setDisplaySegmentStatus(dest=0,segment=seg,status=status)
                    self._writeSystemRecord(user = user,
                                            info = info)
                break
        message = self.segments
        return message


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getDevices(self,dev_no):
        # for key,value in self.devices.items():
        #     d_id = value['id']
        #     d_type = value['type']
        #     d_state = value['status']
        #     d_name = value['name']
        #     stx = self.pm_line.getDeviceState(dev_id = d_id,dev_type=d_type)
        #     if (stx == 'Com Fail') or (stx is None):
        #         state = 2
        #         info = (u'[%s]: 通讯失败' % (d_name))
        #     elif stx == 'Tamper':
        #         state = 1
        #         info = (u'[%s]: 防拆开关打开' % (d_name))
        #     else:
        #         state = 0
        #         info = (u'[%s]: 工作正常' % (d_name))
        #     if d_state != state:
        #         self.devices[key]['status'] = state
        #         self._writeSystemRecord(info = info)

        message = self.devices or {}
        return message

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def setDeviceStatus(self,dev_no,stat):
        d = self.devices
        #dev = str(dev_no)
        dev = str(dev_no)
        st = int(stat)
        user = 'user1@' + cherrypy.request.remote.ip

        for key in d:
            val = d[key]
            if val['name'] == dev:
                dev_id = val['id']
                dev_type = val['type']
                if st == 0 or st == 1:
                    d[key]['secure'] = st
                if st == 1:
                    status = 'Secure'
                    info = (u'布防设备[%s%d]' % (dev_type,dev_id))
                else:
                    status = 'Access'
                    info = (u'撤防设备[%s%d]' % (dev_type,dev_id))
                if self.pm_line is not None:
                    self.pm_line.secureTamper(dev_type = dev_type,dest = dev_id,status=status)
                    self._writeSystemRecord(user = user,
                                            info = info)
        message = self.devices
        return message

    # def setDeviceStatus(self,dev_no,stat):
    #     d = self.devices
    #     dev= int(dev_no)
    #     st = int(stat)
    #     user = 'user1@' + cherrypy.request.remote.ip
    #     for key in d:
    #         val = d[key]
    #         if val['id'] == dev:
    #             if st == 0 or st == 1:
    #                 d[key]['secure'] = st
    #                 if st == 1:
    #                     status = 'Secure'
    #                     info = (u'布防设备[%d]' % dev)
    #                 else:
    #                     status = 'Access'
    #                     info = (u'撤防设备[%d]' % dev)
    #                 if self.pm_line is not None:
    #                     self.pm_line.securePmTamper(dest=dev,status=status)
    #                 self._writeSystemRecord(user = user,
    #                                         info = info)
    #                 break
    #     message = self.devices
    #     return message


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAuxiliaries(self,aux_no):
        message = self.auxiliaries or {}
        return message


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def setAuxiliaryStatus(self,name,stat):
        d = self.auxiliaries
        aux = str(name)
        st = int(stat)
        user = 'user1@' + cherrypy.request.remote.ip
        for key in d:
            val = d[key]
            if val['name'] == aux:
                if st == 0 or st == 1:
                    d[key]['secure'] = st
                    if st == 1:
                        status = 'Secure'
                        info = (u'布防传感器[%s]' % aux)
                    else:
                        status = 'Access'
                        info = (u'撤防传感器[%s]' % aux)
                    if self.pm_line is not None:
                        self.pm_line.secureZone(zone_name=aux,status=status)
                    #log.msg("aux = %r,status=%r" % (aux,status))
                    self._writeSystemRecord(user = user,
                                            info = info)
                    break
        message = self.auxiliaries
        return message

    def _result(self,returns):
        self.log_ready = True
        self.log_datas["data"] = returns

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def getAlarmLogs(self,_):
        self.log_ready = False
        d = self.records.get_records()
        d.addCallback(self._result)
        while self.log_ready is False:
            pass
        return self.log_datas

    ###########################################################################
    #
    #   Sam Engineer Tools
    #
    ###########################################################################

    @cherrypy.expose
    def setup(self):
        main_page = self.temp_setup.render(title='SAM Engineer Tools')
        return main_page

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def putSegments(self):
        result = {"operation": "request", "result": "success"}

        segs = cherrypy.request.json
        self.segments = segs
        return result


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def putDevices(self):
        result = {"operation": "request", "result": "success"}

        self.devices = cherrypy.request.json
        return result

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def putAuxiliaries(self):
        result = {"operation": "request", "result": "success"}

        self.auxiliaries = cherrypy.request.json
        return result


    @cherrypy.expose
    @cherrypy.tools.noBodyProcess()
    def upload(self, theFile=None):
        """upload action
        
        We use our variation of cgi.FieldStorage to parse the MIME
        encoded HTML form data containing the file."""
        
        # the file transfer can take a long time; by default cherrypy
        # limits responses to 300s; we increase it to 1h
        cherrypy.response.timeout = 3600
        
        # convert the header keys to lower case
        lcHDRS = {}
        for key, val in cherrypy.request.headers.iteritems():
            lcHDRS[key.lower()] = val
        
        # at this point we could limit the upload on content-length...
        # incomingBytes = int(lcHDRS['content-length'])
        
        # create our version of cgi.FieldStorage to parse the MIME encoded
        # form data where the file is contained
        formFields = myFieldStorage(fp=cherrypy.request.rfile,
                                    headers=lcHDRS,
                                    environ={'REQUEST_METHOD':'POST'},
                                    keep_blank_values=True)
        
        # we now create a 2nd link to the file, using the submitted
        # filename; if we renamed, there would be a failure because
        # the NamedTemporaryFile, used by our version of cgi.FieldStorage,
        # explicitly deletes the original filename
        theFile = formFields['theFile']
        os.link(theFile.file.name, './data/media/'+theFile.filename)
        
        return "ok, got it filename='%s'" % theFile.filename


    @cherrypy.expose
    def test_upload(self):
        """Simplest possible HTML file upload form. Note that the encoding
        type must be multipart/form-data."""
        
        return """
            <html>
            <body>
                <form action="upload" method="post" enctype="multipart/form-data">
                    File: <input type="file" name="theFile"/> <br/>
                    <input type="submit"/>
                </form>
            </body>
            </html>
            """
    


