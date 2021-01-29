import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse


#IMPORTANTE
#SOLO VA A LA PRIMER PAGINA
#TENGO QUE REACOMODARLO

def googleSearch(query):
    g_clean = []
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    html = requests.get(url)
    if html.status_code==200:
        soup = BeautifulSoup(html.text, 'lxml')
        a = soup.find_all('a')
        for i in a:
            k = i.get('href')
            try:
                m = re.search(r"(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if(re.search('google.com', domain.netloc)):
                    continue
                else:
                    g_clean.append(rul)
            except:
                continue

    #codeblock debajo elimina duplicados
    n = 0
    for link in g_clean:
        cortado = urlparse(link.replace("www.","")).netloc
        g_clean[n] = cortado
        n += 1

    g_clean = list(set(g_clean)) 
    print(g_clean)
    return g_clean



googleSearch('plantas miami')


