from bs4 import BeautifulSoup
import requests
import random
import os

url = "https://www.testious.com/free-cccam-servers/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html.parser")

#find class by name
def match_class(target):
    def do_match(tag):
        classes = tag.get('class', [])
        return all(c in classes for c in target)
    return do_match

cLine = soup.find(match_class(["text"]))
cLine1 = str(cLine)

cLine1 = cLine1.replace("<br/>", "\n")

arrN = []
cArrayFull = []


text = cLine1.split('\n') # split everything into lines.

for line in text:
    if 'N:' in line:
        arrN.append(line)

cUnique = []
cRandom = []
[cUnique.append(item) for item in arrN if item not in cUnique]

N = len(arrN) / 2


cRandom = random.sample(cUnique, N)


#print to file
with open('newcamd.list', mode='wt') as myfile:
    myfile.write('\n'.join(cRandom))

#restart mgcamd
#os.system("killall mgcamd_1.38r1")
#os.system("mgcamd_1.38r1")




print('\n'.join([x.encode('ascii') for x in cRandom]))






