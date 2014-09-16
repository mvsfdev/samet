#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import os
import sqlite3 as lite

class WTable(object):

    def __init__(self,dbase = "www.db"):
        self.conn = lite.connect(dbase)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()
        

    def insertSegment(self,data):
        self.cursor.execute("""
        insert into segment (code,name,x0,y0,x1,y1,secure,status,comment) 
        values (?,?,?,?,?,?,?,?,?)""",data)
        self.conn.commit()
        
    def insertAuxiliary(self,data):
        self.cursor.execute("""
        insert into auxiliary (code,name,x0,y0,x1,y1,x2,y2,x3,y3,secure,status,comment)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",data)
        self.conn.commit()
        
    def insertDevice(self,data):
        self.cursor.execute("""
        insert into device (code,name,x0,y0,x1,y1,secure,status,comment)
        values (?,?,?,?,?,?,?,?,?)""",data)
        self.conn.commit()
        


    def insertTag(self,data):
        self.cursor.execute("""
        insert into tag (code,name,comment ) 
        values (?,?,?)""",data)
        self.conn.commit()
        
    def insertRelay(self,data):
        self.cursor.execute("""
        insert into relay (code,name,comment)
        values (?,?,?)""",data)
        self.conn.commit()

    def getSegments(self):
        query = """
        select * from segment order by id
        """
        seg = self._makeDicts(query)
        seg_json = {}
        for i in seg:
            x_id = i['id'] 
            i['id'] = i['code']
            del i['code']
            seg_json['Seg_' + ('%d' % x_id)] = i
        return seg_json
            
    def getAuxiliaries(self):
        query = """
        select * from auxiliary order by id
        """
        aux = self._makeDicts(query)
        aux_json = {}
        for i in aux:
            x_id = i['id'] 
            i['id'] = i['code']
            del i['code']
            aux_json['Aux_' + ('%d' % x_id)] = i
        return aux_json
            
    def getDevices(self):
        query = """
        select * from device order by id
        """
        dev = self._makeDicts(query)
        dev_json = {}
        for i in dev:
            x_id = i['id'] 
            i['id'] = i['code']
            del i['code']
            dev_json['Dev_' + ('%d' % x_id)] = i
        return dev_json

    def getTags(self):
        query = """
        select code,name from tag order by code
        """
        self.cursor.execute(query)
        tag_list = []
        for row in self.cursor.fetchall():
            code,name = row
            tag_list.append(('tag_' + ('%d' % code),name))
        return tag_list

    def getRelays(self):
        query = """
        select code,name from relay order by code
        """
        self.cursor.execute(query)
        relay_list = []
        for row in self.cursor.fetchall():
            code,name = row
            relay_list.append(('relay_' + ('%d' % code),'relay_off',name))
        return relay_list
        
        
    def _makeDicts(self,query,params=()):
        self.cursor.execute(query,params)
        colnames = [desc[0] for desc in self.cursor.description]
        rowdicts = [dict(zip(colnames,row)) for row in self.cursor.fetchall()]
        return rowdicts

    def finish(self):
        self.cursor.close()
        self.conn.close()
         

if __name__ == '__main__':
    import os.path
    current_dir = os.path.dirname(os.path.abspath(__file__))

    db_path = os.path.join(current_dir, 'data','database','www.db')
    examp = WTable(dbase = db_path)

    segments = [
        {'id': 1, 
         'x0':638,   'y0': 563,    
         'x1':980,   'y1': 720, 
         'name' : u'南墙东段',
        'secure' : 1,
         'status': 0 },

        {'id': 2, 
         'x0':1104,  'y0': 589,    
        'x1':980,   'y1': 720, 
         'name' : u'东墙南段',
         'secure' : 1,
         'status': 0 },
        
        {'id': 3, 
         'x0':1418,  'y0': 259,    
         'x1':1104,   'y1': 589, 
         'name' : u'东墙北段',
         'secure' : 1,
         'status': 0 },


        {'id': 4, 
        'x0':1016,  'y0': 161,    
         'x1':1418,  'y1': 259, 
         'name' : u'北墙',
         'secure' : 1,
        'status': 0 },
        
        {'id': 5,
         'x0':780,   'y0': 296, 
         'x1':1016,  'y1': 161, 
         'name' : u'西墙北段',
         'secure' : 1,
         'status': 0 },

        {'id': 6,
         'x0':457,   'y0': 480, 
         'x1':780,   'y1': 296,   
         'name' : u'西墙南段',
         'secure' : 1,
        'status': 0 },

        {'id': 7, 
         'x0':567,   'y0': 533,    
         'x1':457,   'y1': 480, 
         'name' : u'南墙西段',
         'secure' : 1,
         'status': 0 },
        
    ]


    for i in segments:
        data = (i['id'],
                i['name'],
                i['x0'],
                i['y0'],
                i['x1'],
                i['y1'],
                i['secure'],
                i['status'],
                'Seg_' + ('%d' % i['id']))
        examp.insertSegment(data)


    auxiliaries = [
        {'id': 1, 
         'x0': 629,   'y0': 590, 
         'x1': 633,   'y1': 620, 
         'x2': 571,   'y2': 588, 
         'x3': 566,   'y3': 558, 
         'name': u'大门',
         'secure' : 1,
         'status': 0 },

        {'id': 2, 
         'x0': 865,  'y0': 425,  
         'x1': 803,  'y1': 402,
         'x2': 804,  'y2': 431,
         'x3': 866,  'y3': 454,  
         'name': u'工艺区门',
         'secure' : 1,
         'status': 0 },

    ]

    for i in auxiliaries:
        data = (i['id'],
                i['name'],
                i['x0'],
                i['y0'],
                i['x1'],
                i['y1'],
                i['x2'],
                i['y2'],
                i['x3'],
                i['y3'],
                i['secure'],
                i['status'],
                'Aux_' + ('%d' % i['id']))
        examp.insertAuxiliary(data)

    devices = [
        {'id': 1, 
         'x0': 30,  'y0': 60,  
         'x1': 80,  'y1': 88,
         'name': u'PM1',
         'secure' : 1,
         'status': 0 },

        {'id': 2, 
         'x0': 30,  'y0': 100,  
         'x1': 80,  'y1': 128,
         'name': u'PM2',
        'secure' : 1,
         'status': 0 },

        {'id': 3, 
         'x0': 30,  'y0': 140,  
         'x1': 80,  'y1': 168,
         'name': u'PM3',
         'secure' : 1,
         'status': 0 },

    ]
        

    for i in devices:
        data = (i['id'],
                i['name'],
                i['x0'],
                i['y0'],
                i['x1'],
                i['y1'],
                i['secure'],
                i['status'],
                'Dev_' + ('%d' % i['id']))
        examp.insertDevice(data)

    print examp.getSegments()
    print examp.getAuxiliaries()
    print examp.getDevices()
    print examp.getTags()
    print examp.getRelays()

    examp.finish()

