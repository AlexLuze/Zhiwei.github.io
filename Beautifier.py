#-*-coding:utf-8 -*-
# !/usr/bin/env python
# Author: AlexLuze
# IDE: PyCharm
# CreateTime: 2018/12/5
print "This is second git File for Zhiwei repositories."
from PySide2 import QtWidgets,QtCore
import traceback
import time

class TextProgressDialog(QtWidgets.QLabel):
    '''A dialog to show the progress of the process.'''
    
    def __init__(self, text, action, args=[], kwargs={}, waitSeconds=1, parent=None):
        '''If the passed time is greater then waitSeconds, the dialog will pop up.'''
        
        self._text = text + ' '
        self._action = action
        self._args = args
        self._kwargs = kwargs
        self._actionReturned = None
        self._actionFinished = False
        self._actionFailed = False
        self._actionException = ''
        self._thread = None
        
        self._waitSeconds = waitSeconds
        self._sleepSecond = 0.13
        self._progressTextCount = 8
        self._progressText = '>' * self._progressTextCount
        self._suffix = ''
        self._go = True
        
        self._app = QtWidgets.QApplication.instance()
        
        QtWidgets.QLabel.__init__(self, parent)
        self.setWindowTitle('Progress')
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(QtCore.Qt.Dialog)
        # self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint)
        # self.setWindowFlags(QtCore.Qt.Popup)
        
        s = 'background-color: #343434; padding: 30'
        self.setStyleSheet(s)

        # x = 0.5*self._app.desktop().width() - 0.5*self.width()
        # y = 0.5*(self._app.desktop().height() - self.height())
        ##self.move(x, y)
        # self.setGeometry(x, y, self.width(), self.height())
        
        # Set position
        # pos = self.mapToGlobal(parent.pos())
        ##print pos.x(),pos.y()
        #
        # x = pos.x()+0.5*parent.width()
        # y = pos.y()+0.5*parent.height()
        #
        ##x = 0.5*(parent.width()-self.width())
        ##y = 0.5*(parent.height()-self.height())
        # self.setGeometry(x, y, self.width(), self.height())
    
    def closeEvent(self, event):
        self._go = False
        
        QtWidgets.QLabel.closeEvent(self, event)
    
    def _run(self):
        self._thread = QtCore.QThread(self)
        
        def run():
            try:
                self._actionReturned = self._action(*self._args, **self._kwargs)
                self._actionFailed = False
            except:
                self._actionFailed = True
                self._actionException = traceback.format_exc()
            
            self._actionFinished = True
            self._go = False
        
        self._thread.run = run
        self._thread.start()
    
    def start(self):
        # print 'isVisible:',self.isVisible()

        # self.show()

        # print 'isVisible:',self.isVisible()
        
        if self._action:
            self._run()
        
        start = time.time()
        
        while self._go:
            passedTime = time.time() - start
            
            if passedTime >= self._waitSeconds:
                if self.isVisible() == False:
                    self.show()
            
            passedTime = '%d' % passedTime
            suffix = self._suffix.ljust(self._progressTextCount, ' ')
            txt = '%s%s  %s  ' % (self._text, suffix, passedTime)
            
            self.setText(txt)
            self._app.processEvents()
            
            if self._suffix == self._progressText:
                self._suffix = ''
            else:
                self._suffix += '>'
            
            time.sleep(self._sleepSecond)
        
        else:
            self._thread.quit()
            self.close()
            
            if self._actionFailed:
                raiseExceptionDialog(self._actionException)
            
            return self._actionReturned


def showProgress(label='Getting data', waitSeconds=1):
    def call(func):
        def handle(*args, **kwargs):
            progress = TextProgressDialog(label, action=func, args=args, kwargs=kwargs,
                                          waitSeconds=waitSeconds, parent=args[0])
            
            return progress.start()
        
        return handle
    
    return call



