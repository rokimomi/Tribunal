__author__ = 'amine'

# http://stackoverflow.com/questions/12911308/saving-html-with-java-script-output

# -*- coding: utf-8 -*-
import sys, codecs
import os.path as path
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

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

# Grabs 100 tribunal cases starting from 6030454 going down

startingCase = 6030454
caseCount = 100

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

        print 'done | '+str(i+1)+'/'+str(caseCount)+' ('+str(percent)+'%)'

    startingCase -= 1

print 'Done!'



