# This script scrapes publicly available information and attempts to extract 
# indidividual id. 

from bs4 import BeautifulSoup
import sys
import urllib2
import unicodedata
import operator

url_to_get = "https://www.linkedin.com/in/michaelshaughnessy1"
github_urls = ["https://github.com/mickeyshaughnessy"]
dir_urls = ["https://www.linkedin.com/pub/dir/David/Culver", "https://www.linkedin.com/pub/dir/Gabe/Shaughnessy"]
urls_to_get = [
    "https://www.linkedin.com/in/mark-thompson-93337825", 
    "https://www.linkedin.com/in/successmatters", 
    "https://uk.linkedin.com/in/mark-thompson-b4500024"]
    

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36')]
li_company_page = opener.open(url_to_get).read()
#li_company_page = opener.open(github_urls[0]).read()

soup = BeautifulSoup(li_company_page.decode('utf-8', 'ignore'))
visible_text = soup.getText()
visible_text = unicodedata.normalize('NFKD', visible_text).encode('ascii','ignore')
print len(visible_text)
all_text = ''.join(visible_text)
#print visible_text
#raw_input()


#[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
sep_chars1 = ['\n', '.', ',', '"', ';', '?', '!', '[', ']', '{', '}', "'", '-',
                           '+', '^', '(', ')', ':', '_', '=']
sep_chars2 = ['\n', '.', ',', '"', ';', '?', '!', '[', ']', '{', '}',
                           '+', '^', '(', ')', ':', '_', '=', '/']
for c in sep_chars2:
    all_text = all_text.replace(c,' ')
print all_text
raw_input()
all_text = ' '.join(all_text.split())
all_text = all_text.lower()
all_text = all_text.split()

N = 3
Ngrams = {}
for i in xrange(len(all_text) - (N+1)):
    gram = ' '.join([all_text[i+x] for x in xrange(N)])
    if Ngrams.get(gram):
        Ngrams[gram] += 1
    else:
        Ngrams[gram] = 1

sorted_N = sorted(Ngrams.items(), key=operator.itemgetter(1))
print 'Top 10 N grams are:'
for i in range(1,11):
    print '"%s", count: %s' % (sorted_N[-i][0], sorted_N[-i][1])
