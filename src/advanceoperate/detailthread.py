#coding=utf-8

import sys, os
from PyQt4 import QtCore
sys.path.append("..")
from publicfunc.fileanalyze import PEFileAnalize, getFileInfo

class FileDetail(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, filename, parent=None):
        super(FileDetail, self).__init__(parent)
        self.filename = str(filename)

    def run(self):
        # 获取文件基本内容
        useless, baseinfo = getFileInfo(self.filename)
        self.finishSignal.emit(baseinfo)

class PEFileInfo(QtCore.QThread):
    finishSignal = QtCore.pyqtSignal(list)

    def __init__(self, filename, parent=None):
        super(PEFileInfo, self).__init__(parent)
        self.filename = str(filename)

    def getPEInfo(self):
        pefile  = PEFileAnalize(self.filename)
        secinfo = pefile.checkFileSections()
        return secinfo

    def run(self):
        print "pefile info from thread"
        self.finishSignal.emit(self.getPEInfo())
