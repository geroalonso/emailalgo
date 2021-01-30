import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
from urllib.parse import urlparse
import re


emails = []



def lengthofset(setlist):
  counter = 0
  for i in set(setlist):
    counter += 1

  return counter



def localurlchecker(trial, site):
	test = urlparse(trial.replace("www.","")).netloc
	base = urlparse(site.replace("www.","")).netloc

	if base == test:
		return True

	else:
		return False

#Making the request with requests
def openscrape(url):
	'''This function algorithm is the following:
      1) opens the url defined in the parameter
      2) scrape for emails in said url.
      3) save the emails into a global list
      4) finds all links in url, hereby defined as children
      5) saves children into a list '''

	#make the request to the server
	headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
	}
	response = requests.get(url, headers = headers)
	response_text = response.text
	#parsing the data with beautiful soup
	soup = BeautifulSoup(response_text, 'html.parser')

#[\w\.-]+@+[\w\.-]+

	#scrape for the emails
	emails.extend(list(set(re.findall(r'[\w\.-]+@+[\w\.-]+[.com]', response_text)))) #regex to search emails 
	#scrape for the links in the site
	href_list = []
	links = soup.find_all('a')
	for link in links:
		href = urljoin(url,link.get('href'))
		if localurlchecker(href, url) == True:
			href_list.append(href)
		else:
			pass
	return href_list



def crawling(baseurl):
  global emails 
  emails = []
  graph = {}
  visited = []
  queue = []
  visited.append(baseurl)
  queue.append(baseurl)
  while queue:
    try:
      s = queue.pop(0)
      openscrape(s)
      print(s)
      graph[s] = openscrape(s)
      for hijo in graph[s]:
        if hijo not in visited:
          visited.append(hijo)
          queue.append(hijo)
    except:
      continue

  with open('emails.txt', 'a') as f:
    for item in set(emails):
      f.write(item + '\n')



print('arranca')



