# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from MS_MainWindow import Ui_MainWindow
import sys, os, shutil
from tabletest import checkFolder

reload(sys)
sys.setdefaultencoding( "utf-8" )

class MainWindow(QtGui.QMainWindow):
    scanemit = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.table = self.ui.tableWidget
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        self.folder = ''
        self.dir = ''
        self.table = self.ui.tableWidget
        self.rowindex = 0

        QtCore.QObject.connect(self.ui.PB_SelectFolder, QtCore.SIGNAL("clicked()"), self.selectFolder)
        #QtCore.QObject.connect(self.ui.PB_ScanType, QtCore.SIGNAL("clicked()"), self.iterateFiles)
        self.scanemit.connect(self.recvInitSingal)

    #假设以扫描类型作为开始扫描动作测试
    #需要实现在功能函数线程中而非UI线程
    def selectFolder(self):
        self.folder = QtGui.QFileDialog.getExistingDirectory(self, u"选择文件夹", "e:\\")#QtCore.QDir.currentPath())
        print "lll" + str(self.folder).decode('utf-8')
        if self.folder != '':
            self.folderThread = checkFolder(self.folder)
            # two signals connect one slot
            self.folderThread.numberSignal.connect(self.recvInitSingal)
            self.folderThread.valueSignal.connect(self.recvInitSingal)
            #执行run方法
            self.folderThread.start()

    def recvInitSingal(self, index, msg):
        if 1 == index:
            print "folders number is: " + msg
        if 2 == index:
            print "files number is: " + msg
        if 3 == index:
            self.rowindex = self.rowindex + 1
            i = self.rowindex
            print i
            self.table.setRowCount(i)
            self.table.setItem(i - 1, 0, QtGui.QTableWidgetItem(msg))


    # def iterateFiles(self):
    #     self.dir = os.path.join(str(self.folder).decode('utf-8'))
    #     print self.dir
    #     assert os.path.isdir(self.dir), "make sure this is a path"
    #     result = [] # test print all files
    #     i = 0 # number of files
    #     j = 0 # number of dirs
    #     for root, dirs, files in os.walk(self.dir, topdown=True):
    #         for di in dirs:
    #             j = j + 1
    #             print os.path.join(root, di)
            
    #         for fl in files:
    #             #result.append(os.path.join(root, fl))
    #             i = i + 1
    #             print os.path.join(root, fl)

    #     print "dirs: ",  j
    #     print "files: ", i


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())