
import sys
import xml.etree.ElementTree as ET

class cat_controller(object):
    """docstring for Cat_controller"""

    def __init__(self, arg):
        self.rootPath = ""
        pass

    def init_db(self,year):
        self.doc = ET.parse(os.path.join(rootPath,year+".xml" ))
        self.root = self.doc.getroot()

    def add_video(self,video_data)

