from bs4 import BeautifulSoup
import urllib.request
import time
import random

with open('title.txt', 'r') as f:
    urls = f.read()
    url_list = urls.split('\n')

    for url in url_list:
        file_name = url.split('/')[-1]
        url_open = urllib.request.urlopen(url)
        soup = BeautifulSoup(url_open, 'html.parser')

        title_div = soup.find('div', attrs={'id':'clipInfoArea'})
        title = title_div.find('h3', attrs={'class':'_clipTitle'}).text

        print(url + '\t' + title)

        time.sleep(random.randrange(1,9))