__author__ = 'amine'

# http://stackoverflow.com/questions/12911308/saving-html-with-java-script-output

# -*- coding: utf-8 -*-
import sys, codecs
import os.path as path
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
from datetime import datetime


class Render(QWebPage, QApplication):
  def __init__(self, url, app):
    self.app = app
    QWebPage.__init__(self)
    self.loadFinished.connect(self._loadFinished)
    self.mainFrame().load(QUrl(url))
    self.app.exec_()

  def _loadFinished(self, result):
    self.frame = self.mainFrame()
    self.app.quit()

########################################################################

# Grabs tribunal cases starting from 6030454 going down

startTime = datetime.now()

num_concurrent = 0 # number of concurrently running scripts
offset = 1 # how much to offset the scripts by when running concurrent scrapes


startingCase = 6030454 - offset
caseCount = 10000

# override issues with qt warnings stopping the code
qInstallMsgHandler(None)

app = QApplication(sys.argv)

for i in range(0, caseCount):

    if path.exists("cases/"+str(startingCase)+".html"):

        print 'case '+str(startingCase) + ' scraped already...skipping'

    else:

        print 'grabbing case '+str(startingCase)+'...',

        url = 'http://na.leagueoflegends.com/tribunal/en/case/'+str(startingCase)+'/'
        r = Render(url, app)

        html = unicode(r.frame.toHtml())

        file = open("cases/"+str(startingCase)+".html", "w")

        file.write(html.encode('utf-8'))

        file.close()

        percent = (i+1)/float(caseCount)*100

        timestamp = ""

        if((i+1) % 10 == 0):
         timestamp = datetime.now()-startTime

        print 'done | '+str(i+1)+'/'+str(caseCount)+' ('+str(percent)+'%) ' + str(timestamp)

    startingCase -= (num_concurrent)

print 'Done!'

print(datetime.now()-startTime)



