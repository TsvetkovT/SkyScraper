import requests
from bs4 import BeautifulSoup

query = 'trend'

query = query.replace (" ", "+")

page = requests.get("https://www.google.com/search?q=" +query)
soup = BeautifulSoup(page.content,'lxml')
import re
links = soup.findAll("a")
# for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
   # print re.split(":(?=http)",link["href"].replace("/url?q=",""))


for link in links:
    print link

#print('\n'.join([x.encode('ascii') for x in links]))