# Import the modules
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
import requests



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
             'offset': 50, #es importante cuando quiero hacer requests largos porque pongo desde donde arrancee
             'radius': 20000,
             'location': 'Doral',
             'offset': 0, 
             'limit': 15,
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
lista = []

def webextractoryelp(site):
      chrome_options = Options()  
      chrome_options.add_argument("--headless") 
      chrome_options.add_argument("user-agent= G.Alonso Scraper contact me if my bot is behaving intrusively: geronimoalonso@icloud.com")
      driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) #set the search engine
      driver.get(site)
      urls = driver.find_elements_by_xpath("//a[contains(@href,'url') and @role = 'link']")[1].text
      return urls


for business in business_data['businesses']:
      diccionario = {}
      diccionario ['url'] = business['url']
      diccionario ['phone'] = business['phone']
      diccionario ['location'] = business ['location']['display_address']
      try:
            diccionario ['website'] = webextractoryelp(business['url'])
            print(diccionario['website'])
      except:
            diccionario ['website'] = 'Null'
      lista.append(diccionario)


print(lista) 
#TENGO TODO HASTA ACA, DEBO DEFINIR ANTES DE CORRER EL CODIGO EL OFFSET Y LA CATEGORIA, Y CON ESO ME SACA NOMBRE TELEFONO Y DIRECCION
























