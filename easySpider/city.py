import requests as re
from xml.parsers.expat import ParserCreate


class DefaultSaxHandler(object):
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
    # print (content)
    province = []
    handler = DefaultSaxHandler(province)
    parse = ParserCreate()

    parse.StartElementHandler = handler.start_element
    parse.EndElementHandler = handler.end_element
    parse.CharacterDataHandler = handler.char_date
    
    parse.Parse(content)
    return province


def wirte_to_file(data):
    f = open('pro.cvs', 'w')
    for i in range(len(data)):
        f.writelines(data[i])
        f.writelines("\n")


if __name__ == '__main__':
    url = 'http://www.ip138.com/post'
    data = get_provinenc_entry(url)
    print(len(data))
    wirte_to_file(data)

