import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin 
from urllib.parse import urlparse
import re


emails = []



def localurlchecker(trial, site):
  test = urlparse(trial.replace("www.","")).netloc
  base = urlparse(site.replace("www.","")).netloc

  if base == test:
    return True

  else:
    return False

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

  return emails





# Import the modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
import requests


def webextractoryelp(site):
      chrome_options = Options()  
      chrome_options.add_argument("--headless") 
      chrome_options.add_argument("user-agent= G.Alonso Scraper contact me if my bot is behaving intrusively: geronimoalonso@icloud.com")
      driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #set the search engine
      driver.get(site)
      urls = driver.find_elements_by_xpath("//a[contains(@href,'url') and @role = 'link']")[1].text
      return urls



def yelp():

      # Define a business ID
      unix_time = 1546047836

      # Define my API Key, My Endpoint, and My Header
      API_KEY = 'hOkQ-2smsIUy6xcIhSSJ9x85fV-zzEy8b_ud9McZJtW3MoZ3CjiV9G2POfY4KHbvedtS3OSHuS-Yx4TYe48QgoJzrocKLnB99_Ywg9iUwp3Vd9m-Ukb_BkLg7OUNYHYx'
      ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
      HEADERS = {'Authorization': 'bearer %s' % API_KEY}

      # Define my parameters of the search
      # BUSINESS SEARCH PARAMETERS - EXAMPLE
      PARAMETERS = {'term': 'food',
                   'limit': 3,
                   'offset': 0, #es importante cuando quiero hacer requests largos porque pongo desde donde arrancee
                   'radius': 20000,
                   'location': 'Doral',
                   #'categories': #https://www.yelp.com/developers/documentation/v3/all_category_list
                   }



      # Make a request to the Yelp API
      response = requests.get(url = ENDPOINT,
                              params = PARAMETERS,
                              headers = HEADERS)

      # Conver the JSON String
      business_data = response.json()

      # print the response
      print(json.dumps(business_data, indent = 3))

      #everything will be stored in lista
      conglomerado = []

      for business in business_data['businesses']:
            diccionario = {}
            diccionario ['url'] = business['url']
            diccionario ['phone'] = business['phone']
            diccionario ['location'] = business ['location']['display_address']
            try:
                  diccionario ['website'] = str('https://www.' + webextractoryelp(business['url']))
                  print(diccionario['website'])
                  diccionario['mails'] = crawling(diccionario ['website'])

            except:
                  diccionario ['website'] = 'Null'
                  diccionario ['email'] = 'Null'
            conglomerado.append(diccionario)

      print(conglomerado)
      return conglomerado 


crawling('https://www.ibericmalls.com')
































































