
from  sys import stdout
import xml.etree.ElementTree as ET

class cat_controller(object):
    """docstring for Cat_controller"""

    def __init__(self, arg):
        self.rootPath = ""
        self.current_year = ""
        self.fields = []
        pass

    def init_db(self,year):
        try:
            self.doc = ET.parse(os.path.join(rootPath,year+".xml" ))
        except IOError as e:
            print " Error : " + e
        self.root = self.doc.getroot()
        self.year = year

    def add_video(self,video_data):
        if not self.root:
            return

        if self.current_year != video_data['year']:
            init_db(video_data['year'])

        video_new_elem = ET.Element("video")
        for field in self.fields:
            t_elem = ET.SubElement(video_new_elem,field)
            t_elem.text = cur_video_data[field]

        self.root.append(video_new_elem)
        save_db()

    def save_db(self):
        self.root.write(stdout)

if __name__ == '__main__':
    test = cat_controller()
