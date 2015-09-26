#!/usr/bin/python
''' impliments catalog video adder '''

import sys
import os
from shutil import copy2

from PySide.QtGui import *
from PySide.QtCore import *
from PySide import QtGui, QtCore
from PySide.phonon import Phonon

from add_ui import Ui_mainWindow
from catalog_controller import CatController

class AddWindow(QMainWindow, Ui_mainWindow):
    """docstring for AddWindow"""

    def __init__(self):
        super(AddWindow, self).__init__()
        #chosen dir path
        self.path = ""
        #list of all videofiles path
        self.pathlist = []
        #curret vide file opened
        self.current_path = ""
        #list of all tasks
        self.task = []
        #final tree relative path
        self.tree_path = os.path.join(os.getcwd(), 'data')
        #db controller
        self.controller = CatController()

        self.setupUi(self)
        self.add_video_widget()
        self.load_values()
        self.set_values()
        self.assign_widgets()
        self.show()

    #display the video widget
    def add_video_widget(self):
        ''' create the video widget'''
        self.media = Phonon.MediaObject(self)
        self.video = Phonon.VideoWidget(self)
        self.video.setGeometry(QtCore.QRect(170, 40, 300, 200))
        Phonon.createPath(self.media, self.video)

    #assign signals to slots
    def assign_widgets(self):
        ''' connect signals and slots or assign callbacks '''
        self.media.stateChanged.connect(self.handle_state_changed)
        self.seekSlider.setMediaObject(self.media)
        self.btn_play.clicked.connect(self.handle_play_button)
        self.btn_folder.clicked.connect(self.handle_button_choose)
        self.btn_nxt.clicked.connect(self.handle_button_next)
        self.btn_add.clicked.connect(self.handle_add_button)

    def handle_add_button(self):
        ''' add button callback '''
        if self.current_path == "":
            return
        year = self.combo_year.currentText()
        task = self.combo_task.currentText()
        ttype = self.combo_type.currentText()
        quality = self.combo_quality.currentText()
        location = self.combo_location.currentText()
        time = self.combo_time.currentText()

        #validate
        v_path = self.move_video(year, task, ttype, location, quality, time)
        v_path = os.path.relpath(v_path)
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
        self.handle_button_next()


    def move_video(self, year, task, ttype, location, quality, time):
        '''move the video to catalog tree, @params:video details'''
        hir_path = os.path.join(self.tree_path, str(year), str(task), \
                   str(ttype), str(location), str(quality), str(time))
        try:
            if not os.path.exists(hir_path):
                os.makedirs(hir_path)
            num = len([name for name in os.listdir(hir_path) if \
                   os.path.isfile(os.path.join(hir_path, name))])
            file_path =  os.path.join(hir_path, str(num) + '.' + str(self.current_path).split('.')[-1])
            copy2(self.current_path,file_path)
            # os.remove(self.current_path)
        except Exception as e:
            print e.args
        else:
            return file_path

    def handle_button_choose(self):
        ''' choose button callback'''
        if self.media.state() == Phonon.PlayingState:
            self.media.stop()
        else:
            dialog = QtGui.QFileDialog(self)
            dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
            if dialog.exec_() == QtGui.QDialog.Accepted:
                self.path = dialog.selectedFiles()[0]
                for root, subfolders, files in os.walk(self.path):
                    for vfile in files:
                        if vfile.split(".")[-1] in ['avi', 'mp4']:
                            self.pathlist.append(os.path.join(self.path, vfile))
            self.handle_button_next()
            dialog.deleteLater()

    def handle_button_next(self):
        ''' callback for next button '''
        if len(self.pathlist) > 0:
            t_path = self.pathlist.pop()
            self.current_path = t_path
            self.label_fileName.setText(os.path.split(t_path)[1])
            self.media.setCurrentSource(Phonon.MediaSource(t_path))
            self.media.play()
        else:
            self.label_fileName.setText("No file")
            self.media.stop()
            self.pathlist = []
            self.current_path = ""
            self.media.clear()
            # TO DO show warniing

    def handle_state_changed(self, newstate, oldstate):
        '''callback for video widget statechange'''
        if newstate == Phonon.PlayingState:
            self.btn_play.setText('pause ||')
        elif newstate == Phonon.PausedState:
            self.btn_play.setText('play >')
        elif (newstate != Phonon.LoadingState and
              newstate != Phonon.BufferingState):
            self.btn_play.setText('play >')
            if newstate == Phonon.ErrorState:
                source = self.media.currentSource().fileName()
                print 'ERROR: could not play: ' +  str(source)
                print str(self.media.errorString())

    def handle_play_button(self):
        ''' play button callback '''
        if self.media.state() == Phonon.PlayingState:
            self.media.pause()
        elif self.media.state() == Phonon.PausedState:
            self.media.play()

    def load_values(self):
        ''' initializes widget values '''
        self.task = ["buoy", 'marker', 'plank', 'torpedo', 'gate', 'parking']
        self.location = ['IITB', 'Transdec']
        self.quality = ['bad', 'okey', 'good']
        self.time = ['morning', 'evening', 'night']
        self.type = ['testing', 'debug']
        self.year = [str(x) for x in range(2011, 2018)]

    def set_values(self):
        ''' set the initialized values into to widgets '''
        self.combo_task.addItems(self.task)
        self.combo_location.addItems(self.location)
        self.combo_quality.addItems(self.quality)
        self.combo_time.addItems(self.time)
        self.combo_year.addItems(self.year)
        self.combo_type.addItems(self.type)



if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MAIN_WIN = AddWindow()
    RET = APP.exec_()
    sys.exit(RET)
