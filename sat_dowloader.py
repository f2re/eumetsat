import requests

base_url = "http://pics.eumetsat.int/images/"
import os
from random import randint
from time import sleep

from lxml.html import fromstring
def get_proxies():
  url = 'https://free-proxy-list.net/'
  response = requests.get(url)
  parser = fromstring(response.text)
  proxies = set()
  for i in parser.xpath('//tbody/tr')[:10]:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
      #Grabbing IP and corresponding PORT
      proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
      proxies.add(proxy)
  return proxies

def downloadimg(img,path,prox):
  image_url=base_url+img
  sz=0
  if not os.path.isfile(path+img) or  os.path.getsize(path+img)>>20 <1:
      try:
        # img_data = requests.get(image_url,proxies={"http": prox, "https": prox}).content
        img_data = requests.get(image_url).content
      except:
        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
        print("Skipping. Connnection error")
        return 0
      with open(path+img, 'wb') as handler:
        handler.write(img_data)

  sz = os.path.getsize(path+img)>>20 if os.path.isfile(path+img) else 0
  print("size: ",sz)
  if sz<1:
    os.remove(path+img)
  return sz


from datetime import timedelta, date
def daterange(start_date, end_date):
  for n in range(int ((end_date - start_date).days)):
    yield start_date + timedelta(n)


start_date = date(2008, 1, 1)
end_date = date(2010, 1, 1)
# end_date = date(2019, 9, 20)

from itertools import cycle
import traceback

proxies = get_proxies()
print(proxies)
print(len(proxies))
proxy_pool = cycle(proxies)

proxy=""

for single_date in daterange(start_date, end_date):
  # proxy = next(proxy_pool)
  numbers = [1,2,3,4]
  print("STARTING ....",single_date.strftime("%Y%m%d")+"_MSG3.jpg")
  sz = downloadimg( single_date.strftime("%Y%m%d")+"_MSG4.jpg",'./SATTELITE/',proxy )
  if sz<1:
    for j in numbers:
      # proxy = next(proxy_pool)
      sz = downloadimg( single_date.strftime("%Y%m%d")+"_MSG"+str(j)+".jpg",'./SATTELITE/',proxy )
      if sz>=1:
        break
  print("Finished! ",single_date.strftime("%Y-%m-%d"))
  sleep(randint(0,2))