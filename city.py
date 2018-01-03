import requests as re
import xml.etree.cElementTree as ET
from  xml.parsers.expat import ParserCreate

class DeafaultSaxHandler(object):
    def __init__(self, provinence):
        self.provinence = provinence

    def start_element(self, name ,attrs):
        if name != 'map':
            name = attrs['title']
            number = attrs['href']
            self.provinence.append((name, number))

    def end_element(self, name):
        pass

    def char_date(self, text):
        pass


def get_provinenc_entry(url):
    # get content
    content = re.get(url).content.decode('gb2312')
    start = content.find('<map name=\"map_86\" id=\"map_86\">')
    end = content.find('</map>')
    content = content[start:end+len('</map>')].strip()
    print (content)
    # province
    province = []
    handler = DeafaultSaxHandler(province)
    parse = ParserCreate()

    parse.StartElementHandler = handler.start_element
    parse.EndElementHandler = handler.end_element
    parse.CharacterDataHandler = handler.char_date
    
    parse.Parse(content)
    return province

url = 'http://www.ip138.com/post'
p = get_provinenc_entry(url)
print(p)

f = open('pro.cvs','w')



