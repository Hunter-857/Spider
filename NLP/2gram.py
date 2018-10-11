from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string


def ngrams(input, n):
    input = input.split("")
    output = []
    for i in range(len(input) - n+1):
        output.append(input[i:i + n])
    return output


def get_content():
    html = urlopen("http://en.wikipedia.org/wiki/Python")
    bsObj = BeautifulSoup(html)
    content = bsObj.find("div", {"id": "mw-content-text"}).get_text()
    content = cleanInput(content)
    ng = ngrams(content, 2)
    print(ng)
    print("2-grams"+str(len(ng)))


def cleanInput(input):
    input = re.sub('\n+', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInputs = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInputs.append(item)
    return cleanInputs


if __name__ == '__main__':
    get_content()