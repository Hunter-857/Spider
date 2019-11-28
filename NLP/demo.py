from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator


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


def is_common(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with",
                   "on", "do", "say", "this",
                   "they", "is", "an", "at", "but", "we", "his", "from", "that", "not",
                   "by", "she", "or", "as", "what", "go", "their", "can", "who", "get",
                   "if", "would", "her", "all", "my", "make", "about", "know", "will",
                   "as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take",
                   "out", "into", "just", "see", "him", "your", "come", "could", "now",
                   "than", "like", "other", "how", "then", "its", "our", "two", "more",
                   "these", "want", "way", "look", "first", "also", "new", "because",
                    "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
    for word in ngram:
        if word in commonWords:
            return True
    return False


def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input)- n+1):
        ngramTemp = " ".join(input[i:i + n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output


content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
ngram = ngrams(content, 3)
sortedNGrams = []
commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with",
               "on", "do", "say", "this",
               "they", "is", "an", "at", "but", "we", "his", "from", "that", "not",
               "by", "she", "or", "as", "what", "go", "their", "can", "who", "get",
               "if", "would", "her", "all", "my", "make", "about", "know", "will",
               "as", "up", "one", "time", "has", "been", "there", "year", "so",
               "think", "when", "which", "them", "some", "me", "people", "take",
               "out", "into", "just", "see", "him", "your", "come", "could", "now",
               "than", "like", "other", "how", "then", "its", "our", "two", "more",
               "these", "want", "way", "look", "first", "also", "new", "because",
               "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
for word in ngram:
    if word not in commonWords:
        sortedNGrams = sorted(ngram.items(), key=operator.itemgetter(1), reverse=True)
print(sortedNGrams)
