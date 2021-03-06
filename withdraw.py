import pdb
import sys
import MySQLdb
import subprocess
import shlex
import time
from utils import utils
#Simple withdrawal class, processes withdrawals from the database

class withdraw():

    def __init__(self):
        #Set up MySQL cursor
        self.utils = utils()
        self.reddit = self.utils.connect_to_reddit()
        self.cursor = self.utils.get_mysql_cursor()


    def set_confirmed(self,username):
         sql = "UPDATE withdraw SET confirmed=1 WHERE username='%s'" % username
         self.cursor.execute(sql)

    def process_withdrawal(self,address,amount, username):
        if amount.startswith("."):
            amount = "0"+amount
            #pdb.set_trace()
        txid = subprocess.check_output(shlex.split('/home/monotoko/garlic/garlicoin/bin/garlicoin-cli sendtoaddress %s %s' % (address, amount)))
        self.set_confirmed(username)
        print "Sent %s GLC to %s" % (amount, address)
        return txid

    def main(self):
        sql = "SELECT * FROM withdraw WHERE confirmed=0"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        #self.utilsobj.send_messages("ktechmidas","Yo","Test")
        for row in result:
            txid = self.process_withdrawal(row[2], row[3], row[1])
            self.utils.send_message(row[1],"Withdrawal Processed","Hi, this is an automated message to let you know your withdrawal has been processed. The GRLC was sent to %s. \n\nThe TXID is: %s" % (row[2],txid))
        time.sleep(2)

withobj = withdraw()
withobj.main()
