import requests, os
import vk_api, re
import json


home = '/home/o/Изображения/VK/'

vk_session = vk_api.VkApi(
  'login', 
  'passw'
)
headers = {
  'access-control-allow-origin' : '*',
  'Request Method' : 'GET',
  'Status Code' : '200',
  'Remote Address' : '64.233.163.101:443',
  'Referrer Policy' : 'no-referrer-when-downgrade',
  'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

access_token = 'dd990119dd990119dd9901198cddf78823ddd99dd9901198068e6f74798845cfd5d1c15'
api_version = '5.103'

vk_session.auth()    
vk = vk_session.get_api()

album_url = 'https://vk.com/album-63418564_184539412'
album_dir = album_url.replace('https://vk.com/', '')

ids = re.search('album(.*)', album_url).group(1) # https://vk.com/znamenitye_zhenshiny?z=album-63418564_208781310

owner_id = ids.split('_')[0]
album_id = ids.split('_')[1]

# https://vk.com/dev/photos.get
fotos = vk.photos.get(
  owner_id = owner_id,
  album_id = album_id,
  count = 500
)  

# создадим папку для альбома
if not os.path.exists(home + album_dir):
    os.mkdir(home + album_dir, mode=0o777)           
    print('Folder __{}__ created'.format(home + album_dir))
else: 
    print('{} already exists'.format(home + album_dir))

for i in fotos['items']:

  try:
    foto_url = i['sizes'][-1]['url']
    foto_name = foto_url[:-1:8]
    session = requests.Session()
    r = requests.get(foto_url, stream=True)
    image = r.raw.read()
    print(foto_url)
    open(home + album_dir + '/' + foto_name, "wb").write(image)
  
  except (ProtocolError, AttributeError):
      continue
  












'''
#!/usr/bin/env python
# coding: utf-8

# In[74]:


import vk_api
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import requests

vk_session = vk_api.VkApi('89246057878', 'QwasQwasQwas')
vk_session.auth()    
vk = vk_session.get_api()

city = vk.database.getCities(country_id=1, q="Иркутск")
city_id = city['items'][0]['id']


# In[75]:


city_members = vk.users.search(
    city=city_id, 
    count=200,
    fields=[
        'photo_100', 
        'bdate',
        'sex',
        'relations',
        'people_main'
    ]
)

#print(city_members)


# In[76]:


city_members = city_members['items']
all_names = [member['first_name'] for member in city_members]
#print(all_names)

dict_names = dict(Counter(all_names).most_common(10))
names = list(range(len(dict_names)))
values = list(dict_names.values())


# In[82]:


plt.bar(names, values)
plt.xticks(names, dict_names.keys(), rotation=90);


# In[83]:


def save_pic(url):
    p = requests.get(url)
    out = open('img.jpg', 'wb')
    out.write(p.content)
    out.close()
    return plt.imread('img.jpg')


# In[84]:


plt.imshow(save_pic(city_members[0]['photo_100']))


# In[ ]:





# In[ ]:'''