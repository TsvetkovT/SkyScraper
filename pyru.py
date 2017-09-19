import urllib
from bs4 import BeautifulSoup

try:
    html = urllib.urlopen("https://abv.bg")
except urllib.HTTPError as e:
    print(e)
else:
    bsObj = BeautifulSoup(html.read(),"lxml")


print (bsObj.get_text())