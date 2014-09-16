# _*_ coding: UTF-8 _*_

"""
Usage:
      twistd -n web --wsgi www_app.wsgiapp
"""

import datetime
from twisted.internet import reactor
from twisted.python import log
import cherrypy
from twisted.web.wsgi import WSGIResource

import os.path
current_dir = os.path.dirname(os.path.abspath(__file__))

from www import Root


################ Http Server Start Up ###################################################

#alarm_logs = []
alarm_logs = [(102,  u'2014-06-10 14:49:57',   u'Start Point [28.2] meters',    u'Zone #3',u'L1P1A23'),
              (9876, u'2014-06-11 07:43:22',   u'开始点 [28.2] 米处', 	u'Zone #3',u'L1P1B34')]

from hardcore.database.records import Records
record_path = os.path.join(current_dir,'hardcore','database','alarmlog.db')
myRecords = Records(db_filename=record_path)

from www_table import WTable
db_path = os.path.join(current_dir, 'data','database','www.db')
www_table = WTable(dbase = db_path)



# Create our WSGI app from the CherryPy application
# it will respond to the /blog path
engine_conf_path = os.path.join(current_dir, 'etc','engine.conf')
wsgiapp = cherrypy.tree.mount(Root(myRecords,
                                   alarm_logs = alarm_logs,
                                   wtable=www_table), '/', config=engine_conf_path)

# Configure the CherryPy's app server
# Disable the autoreload which won't play well 
cherrypy.config.update({'engine.autoreload.on': False})

cherrypy.config.update(os.path.join(current_dir, 'etc', 'http.conf'))

# We will be using Twisted HTTP server so let's
# disable the CherryPy's HTTP server entirely
cherrypy.server.unsubscribe()

# If you'd rather use CherryPy's signal handler
# Uncomment the next line. I don't know how well this
# will play with Twisted however
#cherrypy.engine.signals.subscribe()

# Tie our app to Twisted
reactor.addSystemEventTrigger('after', 'startup', cherrypy.engine.start)
reactor.addSystemEventTrigger('before', 'shutdown', cherrypy.engine.exit)
resource = WSGIResource(reactor, reactor.getThreadPool(), wsgiapp)

