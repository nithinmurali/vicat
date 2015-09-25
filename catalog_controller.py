
from  sys import stdout
from os import path, system
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
            self.root = self.doc.getroot()
        except IOError as e:
            print " Error : couldnt find a databse, creating new"
            self.root = ET.Element("catalogData",{'year':year})
            fobj = open(path.join(self.rootPath,year+".xml"),'w')
            fobj.write("<catalogData year='"+year+"'>\n</catalogData>")
        self.current_year = year
        print year

    def add_video(self,video_data):
        if self.current_year != video_data['year']:
            self.init_db(video_data['year'])
        if  self.root is None:
            print "Cant load XML DB\n"
            return
        video_new_elem = ET.Element("video")
        for field in self.fields:
            t_elem = ET.SubElement(video_new_elem,field)
            t_elem.text = video_data[field]
        t_tags = video_data['tags'].split(',')
        for tag in t_tags:
            t_elem = ET.SubElement(video_new_elem,'tag')
            t_elem.text = str(tag)
        self.save_db(video_new_elem)

    def save_db(self,node):
        try:
            rough_string = ET.tostring(node, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            t_tree = reparsed.toprettyxml(indent="\t")
            t_tree = '\n'.join(t_tree.split('\n')[1:])
            system("sed -i '$d' " + path.join(self.rootPath,self.current_year+".xml"))
            f = open(path.join(self.rootPath,self.current_year+".xml"),'a')
            f.write(t_tree)
            f.write("</catalogData>")
        except Exception, e:
            print "Error cant save DB : " + str(e)

if __name__ == '__main__':
    test = cat_controller()
    test.init_db("2011")
