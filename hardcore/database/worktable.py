#!/usr/bin/env python
# _*_ coding: UTF-8 _*_

import os
import sqlite3 as lite

class WorkTable(object):
    '''
    Work Table for processor
    '''

    def __init__(self,db_filename = 'workflow.db'):
        
        ################  about communication Line #########
        self.Lines = {}

        ################  about device  ####################
        self.Devices = {}
        self.NextDevice = 0

        ################  about zone  ######################
        self.Zones = {}
        self.Links = {}
        self.Outputs = {}
        self.Auxiliaries = {}
        
        ############## connect to Database
        self.db = db_filename
        self.conn = lite.connect(db_filename)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()

        ### load Tables from database
        self.loadTables()

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def loadTables(self):
        self._loadLines()
        self._loadDevices()
        self._loadZones()
        self._loadLinks()
        self._loadOutputs()
        self._loadSegments()
        self._loadAuxiliaries()

    def _makeDicts(self,cursor,query,params=()):
        cursor.execute(query,params)
        colnames = [desc[0] for desc in cursor.description]
        rowdicts = [dict(zip(colnames,row)) for row in cursor.fetchall()]
        #return rowdicts
        dicts = {}
        for x in rowdicts:
            dicts[x['id']] = x  
        return dicts

    def _loadLines(self):
        ### Communication Port Table
        self.query = """
                     select *
                     from line 
                     """
        self.Lines = self._makeDicts(self.cursor,self.query)

    def _loadSegments(self):
        ### Segment Table
        self.query = """
                     select *
                     from segment 
                     """
        self.Segments = self._makeDicts(self.cursor,self.query)

    def deleteSegments(self,line):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()

        query = "delete from segment where line=%d" % line

        self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()



    def insertSegment(self,data):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
        insert into segment (line,seg_no,unit,wing,start_cell,end_cell,reserved)
        values (?,?,?,?,?,?,?)""",data)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def _loadAuxiliaries(self):
        ### auxiliary Table
        self.query = """
                     select *
                     from auxiliary 
                     """
        self.Auxiliaries = self._makeDicts(self.cursor,self.query)

    def deleteAuxiliaries(self,line):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()

        query = "delete from auxiliary where line=%d" % line

        self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


    def insertAuxiliary(self,data):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("""
        insert into auxiliary (line,aux_no,unit,unit_type,point)
        values (?,?,?,?,?)""",data)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()


    def _loadDevices(self):
        self.NumberOfDevices = 0
        ### Device Table
        self.query = """
                     select *
                     from device 
                     """
        self.Devices = self._makeDicts(self.cursor,self.query)

    def _loadZones(self):
        ### Zone Table
        self.query = """
                     select *
                     from zone 
                     """
        self.Zones = self._makeDicts(self.cursor,self.query)

    def deleteZones(self,line):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()

        query = "delete from zone where line=%d" % line

        self.cursor.execute(query)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def insertZone(self,data):
        ############## connect to Database
        self.conn = lite.connect(self.db)
        self.conn.row_factory = lite.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        insert into zone (line,number,unit,wing,start,end,state)
        values (?,?,?,?,?,?,?)""",data)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()



    def whichZone(self,point):
        ### use gived alarm point to find Zone
        for zone in self.Zones:
            if (zone['device'] == point['unit'] and
                zone['input_type'] == point['type'] and
                zone['wing'] == point['wing'] and 
                (zone['start_cell'] <= point['location'] <= zone['end_cell'] or
                 zone['start_cell'] >= point['location'] >= zone['end_cell']) and
                zone['input'] == point['input']):
                return zone

    def getDeviceByName(self,zone_name):
        if zone_name is None:
            return None
        for zone in self.Zones:
            if(zone['name'] == zone_name):
                info = (zone['id'],zone['device'],zone['input_type'],zone['wing'],zone['start_cell'],zone['end_cell'],zone['input'])
                return info
        return None

    def whichRelay(self,zone):
        relays = []
        rt = False
        for link in self.Links:
            if(link['zone'] == zone):
                out_id = link['output']
                try:
                    (dev,jun)  = self.whichOutput(out_id)
                except:
                    dev = None
                    jun = None
                if((dev is not None) and (jun is not None)):
                    relays.append((dev,jun))
                    rt = True
        if rt is True:
            return relays
        else:
            return None

    def whichOutput(self,xid):
        for out in self.Outputs:
            if(out['id'] == xid):
                return (out['device'],out['junction'])
        return None


    def getDevicesByLine(self,line):
        return_devices = []
        for dev in self.Devices:
            if dev['line'] == line:
                return_devices.append((dev['address'],dev['type'],'Running',0,0,dev['host'],0))
        return return_devices


    def _loadLinks(self):
        ### Link Table
        self.query = """
                     select *
                     from link 
                     """
        self.Links = self._makeDicts(self.cursor,self.query)


    def _loadOutputs(self):
        ### Output Table
        self.query = """
                     select *
                     from output 
                     """
        self.Outputs = self._makeDicts(self.cursor,self.query)

    def _viewHex(self,s):
        if s:
            return str.join("",("%02X " % ord(i) for i in s))


    def _printHex(self,head,s):
        print head, str.join("",("%02X " % ord(i) for i in s))


if __name__ == '__main__':
    print "Hi! Guys, I'm WorkTable module, and you are? I'm so happy,beac se..."

    wt = WorkTable('workflow.db')
    
    print wt.Lines
    print wt.Devices
    print wt.Zones
    print wt.Links
    print wt.Outputs
    print wt.Segments
    print wt.Auxiliaries

    print wt.getDevicesByLine(1)
