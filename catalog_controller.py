
from  sys import stdout
from os import path
import xml.etree.ElementTree as ET
from xml.dom import minidom

class cat_controller(object):
    """docstring for Cat_controller"""

    def __init__(self):
        self.rootPath = "./databases"
        self.current_year = ""
        self.fields = ['path', 'task', 'type', 'quality', 'location',
                     'time', 'false', 'pass', 'perseen']

    def init_db(self,year):
        try:
            self.doc = ET.parse(path.join(self.rootPath,year+".xml" ))
        except IOError as e:
            print " Error : " + str(e)
        self.root = self.doc.getroot()
        self.current_year = year

    def add_video(self,video_data):
        if self.current_year != video_data['year']:
            self.init_db(video_data['year'])
        if not self.root:
            return
        video_new_elem = ET.Element("video")
        for field in self.fields:
            t_elem = ET.SubElement(video_new_elem,field)
            t_elem.text = video_data[field]
        self.root.append(video_new_elem)
        self.save_db()

    def save_db(self):
        try:
            rough_string = ElementTree.tostring(elem, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            t_tree = reparsed.toprettyxml(indent="\t")
            f = open(path.join(self.rootPath,self.current_year+".xml"))
            f.write(t_tree)
        except Exception, e:
            print str(e)

if __name__ == '__main__':
    test = cat_controller()
    test.init_db("2015")
