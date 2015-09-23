import sys
import os
from shutil import copy2

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtGui, QtCore
from PySide.phonon import Phonon

from add_ui import Ui_mainWindow

class addWindow(QMainWindow,Ui_mainWindow):
    """docstring for addWindow"""
    
    def __init__(self):
        super(addWindow, self).__init__()
        #chosen dir path
        self.path = ""
        #list of all videofiles path
        self.pathlist = []
        #curret vide file opened
        self.currentPath = ""
        #list of all tasks
        self.task = []
        #final tree
        self.tree_path = os.getcwd()

        #database path
        self.db_path = ''

        self.setupUi(self)
        self.addVideo_widget()
        self.loadValues()
        self.setValues()
        self.assignWidgets()
        self.show()

    #display the video widget
    def addVideo_widget(self):
        self.media = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget(self)
        self.video.setGeometry(QtCore.QRect(170, 40, 300, 200))
        Phonon.createPath(self.media, self.video)

    #assign signals to slots
    def assignWidgets(self):
        self.media.stateChanged.connect(self.handleStateChanged)
        self.seekSlider.setMediaObject( self.media )
        self.btn_play.clicked.connect( self.handlePlayButton )
        self.btn_folder.clicked.connect( self.handleButtonChoose )
        self.btn_nxt.clicked.connect( self.handleNextbutton )
    
    def handleButtonChoose(self):
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            dialog = QtGui.QFileDialog(self)
            dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                self.path = dialog.selectedFiles()[0]
                for file in os.listdir(self.path):
                    if file.endswith(".avi") or file.endswith(".avi"):
                        self.pathlist.append( os.path.join(self.path, file) )
            self.handleNextbutton()
            dialog.deleteLater()
    
    def handleNextbutton(self):
        if len(self.pathlist)>0:
            t_path = self.pathlist.pop()
            self.label_fileName.setText(os.path.split(t_path)[1])
            self.media.setCurrentSource(Phonon.MediaSource(t_path))
            self.media.play()
        else:
            self.label_fileName.setText("No file")
            self.media.stop()
            self.media.clear()
            # TO DO show warniing

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.btn_play.setText('pause ||')
        elif newstate == Phonon.PausedState:
            self.btn_play.setText('play >')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.btn_play.setText('play >')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print ('ERROR: could not play: %s' % source)
                print ('  %s' % self.media.errorString())

    def handlePlayButton(self):
        if self.media.state() == Phonon.PlayingState :
            self.media.pause()
        elif self.media.state() == Phonon.PausedState :
            self.media.play()

    def loadValues(self):
        self.task = ["buoy",'marker','plank','torpedo','gate','parking']
        self.location = ['IITB','Transdec']
        self.quality = ['1','2','3','4','5']
        self.time = ['morning', 'evening', 'night']
        self.type = ['testing','debug']
        self.year = [ str(x) for x in range(2011,2020) ]

    def setValues(self):
        self.combo_task.addItems(self.task)
        self.combo_location.addItems(self.location)
        self.combo_quality.addItems(self.quality)
        self.combo_time.addItems(self.time)
        self.combo_year.addItems(self.year)
        self.combo_type.addItems(self.type)

    def move_video(self,year,task,ttype,quality,time):
        hir_path = os.path.join(self.tree_path,year,task,ttype,quality,time)
        try:
            if not os.path.exists(hir_path):
                os.makedirs(hir_path)
            shutil.copy2(self.currentPath,os.path.join(hir_path, os.path.split(currentPath)[1] ))
        except Exception, e:
            print e.args


if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWin = addWindow()
   ret = app.exec_()
   sys.exit( ret )
