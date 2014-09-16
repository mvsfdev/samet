from twisted.internet import reactor
from twisted.enterprise import adbapi
from twisted.python import log

class Records(object):

    def __init__(self,db_filename="alarmlog.db"):
        """
        Connect to the database in the pool.

        .. note:: hardcoded db settings
        """
        self.dbpool = adbapi.ConnectionPool("sqlite3", 
                                            db_filename,
                                            check_same_thread=False)
        self.lastrowid = 1

    def process_item(self,item):
        """
        Run db query in thread pool and call :func:`_conditional_insert`.

        :param spider: The spider that created the Item
        :type spider:  spider
        :param item: The Item to process
        :type item: Item
        :returns:  Item
        """
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._database_error, item)
        #query.addCallback(self._result)
        return query
        #return item

    def _conditional_insert(self, tx, item):
        """
        Insert an entry in the `log` table 

        :param tx: Database cursor
        :param item: The Item to process
        :type item: Item
        """
        if not item['id']:
            log.msg("Inserting into Record table: (%s,%s,%s,%s,%s,%s,%s) " % 
                    (item['occured'],item['description'],item['details'],item['operator'],item['disposition'],item['tag'],item['comment']))
            tx.execute(\
                       "insert into event (occured,description,details,operator,disposition,tag,comment) values (? ,?,?,?,?,?,?)",
                       (
                           item['occured'],
                           item['description'],
                           item['details'],
                           item['operator'],
                           item['disposition'],
                           item['tag'],
                           item['comment']
                       ) )
            self.lastrowid = tx.lastrowid
            item['id'] = tx.lastrowid
            #return {'lastrowid':tx.lastrowid}
            return item
        else:
            return None

    def get_records(self,item=None):
        """
        Run db query in thread pool and call :func:`_conditional_insert`.

        :param spider: The spider that created the Item
        :type spider:  spider
        :param item: The Item to process
        :type item: Item
        :returns:  Item
        """
        query = self.dbpool.runInteraction(self._query_records, item)
        #query.addErrback(self._database_error, item)
        #query.addCallback(self._result)
        return query
        #return item


    def _query_records(self, tx, item):
        """
        Insert an entry in the `log` table 

        :param tx: Database cursor
        :param item: The Item to process
        :type item: Item
        """
        tx.execute("SELECT * FROM event")
        #result = tx.fetchone()
        result = []
        for row in tx.fetchall():
            result.append(list(row))
        return result

    def _result(self,returns):
        print "The result is:"
        print returns

    def _database_error(self, e, item):
        """
        Log an exception to the Scrapy log buffer.
        """
        print "Database error: ", e

    def finish(self):
        self.dbpool.close()


if __name__ == '__main__':

    updated = False
    def printResult(returns):
        updated = True
        print updated,returns

    import sys
    logFile = sys.stdout
    log.startLogging(logFile)
    
    d = Records()
    x = {'id':None,
         'occured': "2014-05-04 13:40:13",
         'description':"East wall intruder!",
         'details':'1-1-23',
         'operator': 1,
         'disposition': "2014-05-04 13:40:13",
         'tag' : 1,
         'comment': 'no comment'
         }
    d.process_item(x).addCallback(printResult)
    #d.process_item(x)
    
    d.get_records()

    reactor.callLater(3, d.finish)
    reactor.callLater(3, reactor.stop)
    reactor.run()
