'''Model class for handling XML databases for vicat'''

from os import path, system
import xml.etree.ElementTree as ET
from xml.dom import minidom

class CatController(object):
    """docstring for CatController"""

    def __init__(self):
        self.root_path = "./databases"
        self.current_year = ""
        self.fields = ['path', 'task', 'type', 'quality', 'location', \
                     'time', 'false', 'pass', 'perseen']

    def init_db(self, year):
        '''initilie the database according to the year'''
        try:
            self.doc = ET.parse(path.join(self.root_path, year+".xml"))
            self.root = self.doc.getroot()
        except IOError:
            print " WARNING : couldnt find a databse, creating new"
            self.root = ET.Element("catalogData", {'year':year})
            fobj = open(path.join(self.root_path, year+".xml"), 'w')
            fobj.write("<catalogData year='"+year+"'>\n</catalogData>")
        self.current_year = year

    def add_video(self, video_data):
        ''' add an new video entry to corresponding database'''
        if self.current_year != video_data['year']:
            self.init_db(video_data['year'])
        if  self.root is None:
            print "Cant load XML DB\n"
            return
        video_new_elem = ET.Element("video")
        for field in self.fields:
            t_elem = ET.SubElement(video_new_elem, field)
            t_elem.text = video_data[field]
        t_tags = video_data['tags'].split(',')
        for tag in t_tags:
            t_elem = ET.SubElement(video_new_elem, 'tag')
            t_elem.text = str(tag)
        self.save_db(video_new_elem)

    def save_db(self, node):
        '''save changes to the opened database'''
        try:
            rough_string = ET.tostring(node, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            t_tree = reparsed.toprettyxml(indent="\t")
            t_tree = '\n'.join(t_tree.split('\n')[1:])
            system("sed -i '$d' " + path.join(self.root_path, self.current_year+".xml"))
            db_file = open(path.join(self.root_path, self.current_year+".xml"), 'a')
            db_file.write(t_tree)
            db_file.write("</catalogData>")
        except IOError as ioerr:
            print "Error cant save DB : " + str(ioerr)

#debug
# if __name__ == '__main__':
#     test = CatController()
#     test.init_db("2011")
