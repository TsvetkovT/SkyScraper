# -*- coding: utf-8 -*-

import time
import urllib as urllib
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class Browser:

    def __init__(self, path, initiate=True, implicit_wait_time = 10, explicit_wait_time = 2):
        self.path = path
        self.implicit_wait_time = implicit_wait_time    # http://www.aptuz.com/blog/selenium-implicit-vs-explicit-waits/
        self.explicit_wait_time = explicit_wait_time    # http://www.aptuz.com/blog/selenium-implicit-vs-explicit-waits/
        if initiate:
            self.start()
        return

    def start(self):
        self.driver = webdriver.PhantomJS(path)
        self.driver.implicitly_wait(self.implicit_wait_time)
        return

    def end(self):
        self.driver.quit()
        return

    def go_to_url(self, url, wait_time = None):
        if wait_time is None:
            wait_time = self.explicit_wait_time
        self.driver.get(url)
        print('[*] Fetching results from: {}'.format(url))
        time.sleep(wait_time)
        return

    def get_search_url(self, query, page_num=0, per_page=10, lang='en'):
        query = urllib.pathname2url(query)
        url = 'https://www.google.com/search?q={}&num={}&start={}&nl={}'.format(query, per_page, page_num*per_page, lang)
        return url

    def scrape(self):
        #xpath migth change in future
        links = self.driver.find_elements_by_xpath("//h3[@class='r']/a[@href]") # searches for all links insede h3 tags with class "r"
        results = []
        for link in links:
            d = {'url': link.get_attribute('href'),
                 'title': link.text}
            results.append(d)
        return results

    def search(self, query, page_num=0, per_page=8, lang='en', wait_time = None):
        if wait_time is None:
            wait_time = self.explicit_wait_time
        url = self.get_search_url(query, page_num, per_page, lang)
        self.go_to_url(url, wait_time)
        results = self.scrape()
        return results


sQuery = raw_input("Please enter your Google search string: ")

#path = '/usr/bin/phantomjs' ## SET YOU PATH TO phantomjs
path = '/Applications/phantomjs/bin/phantomjs' ## SET YOU PATH TO phantomjs

br = Browser(path)
results = br.search((sQuery).encode('utf-8'))
#scraped = br.scrape(results)
#create urlList (results)

urlList = []


for r in results:
    urlList.append(r['url'])


br.end()

#reading the content from urlList

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

req = []
soup = []
textFiltered = []

for url in urlList:
    req.append(requests.get(url, headers=headers))

for iReq in req:
    #soup.append(BeautifulSoup(iReq.text, "html.parser"))
    soup.append(BeautifulSoup(iReq.text, "html.parser"))




#clearing out html and retreiving the pure text

INVISIBLE_ELEMS = ('style', 'script', 'head', 'title')
RE_SPACES = re.compile(r'\s{3,}')

def visible_texts(soup):
    """ get visible text from a document """
    text = ' '.join([
        s for s in soup.strings
        if s.parent.name not in INVISIBLE_ELEMS
    ])
    # collapse multiple spaces to two spaces.
    return RE_SPACES.sub('  ', text)

#Clear html and make it text:
TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'li']

def html_to_text(s):
    for tag in s.find_all(TAGS):
        yield tag.get_text()


result = []


for iSoup in soup:
    for x in html_to_text(iSoup):
        result.append(x)
        print ((x.encode('utf-8')))
    #for elem in iSoup(text=re.compile(r""+sQuery, re.MULTILINE)):
        #print elem.parent



'''

for content in soup:
    textFiltered.append(visible_texts(content))

print (len(textFiltered))
print ('\n'+'\n'.join([x for x in textFiltered]))
print ('\n'+'\n'.join(textFiltered))

'''

'''

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

'''