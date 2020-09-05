import requests, os
import vk_api, re
import json


access_token = ''
api_version = '5.122'

owner_id = '-68046969'

home = 'G:/Desktop/py/' + owner_id[1:] + '/'
txt = 'G:/Desktop/py/' + owner_id[1:] + '/' + owner_id[1:] + '.txt' 

if not os.path.exists(home):
    os.mkdir(home, mode=0o777)           
    print('Folder __{}__ created'.format(home))
else: 
    print('{} already exists'.format(home))

f = open(txt, 'w')

vk_session = vk_api.VkApi(
  'num', 
  'passw'
)

vk_session.auth()    
vk = vk_session.get_api()

albums = vk.photos.getAlbums(owner_id = owner_id)['items']

for _ in albums:
    # id of album
    album_id = _['id']

    fotos = vk.photos.get(
        owner_id = owner_id,
        album_id = album_id,
        count = 999
    )

    foto_url = fotos['items'][0]['sizes'][-1]['url']

    f.write(foto_url + '\n')
    print(foto_url)

f.close()

