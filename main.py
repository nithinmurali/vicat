#!/usr/bin/python

import sys
import os
from shutil import copy2

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtGui, QtCore
from PySide.phonon import Phonon

from add_ui import Ui_mainWindow
from catalog_controller import cat_controller

class addWindow(QMainWindow, Ui_mainWindow):
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
        #final tree relative path
        self.tree_path = os.path.join(os.getcwd(),'data')

        #db controller
        self.controller = cat_controller()

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
        self.btn_add.clicked.connect( self.handleAddButton )

    def handleAddButton(self):
        if self.currentPath == "":
            return
        year =  self.combo_year.currentText()
        task = self.combo_task.currentText()
        ttype = self.combo_type.currentText()
        quality = self.combo_quality.currentText()
        location = self.combo_location.currentText()
        time = self.combo_time.currentText()

        #validate
        v_path = self.move_video(year, task, ttype, location, quality, time)
        v_path = os.path.relpath(v_path)
        print v_path
        video_data = {
            'path':v_path,
            'year':year,
            'task':task,
            'type':ttype,
            'quality':quality,
            'location':location,
            'time':time,
            'tags':str(self.line_tags.text()),
            'false':str(self.check_false.isChecked()),
            'pass':str(self.check_pass.isChecked()),
            'perseen':str(self.slider_seen.value())
        }
        self.controller.add_video(video_data)
        self.handleNextbutton()


    def move_video(self, year, task, ttype, location, quality, time):
        hir_path = os.path.join(self.tree_path, str(year), str(task), str(ttype), str(location), str(quality), str(time))
        try:
            if not os.path.exists(hir_path):
                os.makedirs(hir_path)
            num = len([name for name in os.listdir(hir_path) if os.path.isfile(os.path.join(hir_path, name))])
            copy2(self.currentPath,os.path.join(hir_path, os.path.split(self.currentPath)[1]))
            # os.remove(self.currentPath)
        except Exception as e:
            print e.args
        else:
            return hir_path

    def handleButtonChoose(self):
        ''' dfdfdfdf '''
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
            self.currentPath = t_path
            self.label_fileName.setText(os.path.split(t_path)[1])
            self.media.setCurrentSource(Phonon.MediaSource(t_path))
            self.media.play()
        else:
            self.label_fileName.setText("No file")
            self.media.stop()
            self.pathlist = []
            self.currentPath = ""
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
        self.quality = ['bad','okey','good']
        self.time = ['morning', 'evening', 'night']
        self.type = ['testing','debug']
        self.year = [ str(x) for x in range(2011,2018) ]

    def setValues(self):
        self.combo_task.addItems(self.task)
        self.combo_location.addItems(self.location)
        self.combo_quality.addItems(self.quality)
        self.combo_time.addItems(self.time)
        self.combo_year.addItems(self.year)
        self.combo_type.addItems(self.type)



if __name__ == '__main__':
   app = QApplication(sys.argv)
   mainWin = addWindow()
   ret = app.exec_()
   sys.exit( ret )
