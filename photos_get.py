import requests, os
import vk_api, re
import json


home = '/home/o/Документы/PYTHON_SCRIPTS/vk/'

vk_session = vk_api.VkApi(
  'phone', 
  'pass'
)
headers = {
  'access-control-allow-origin' : '*',
  'Request Method' : 'GET',
  'Status Code' : '200',
  'Remote Address' : '64.233.163.101:443',
  'Referrer Policy' : 'no-referrer-when-downgrade',
  'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

access_token = ''
api_version = '5.103'

vk_session.auth()    
vk = vk_session.get_api()

album_urls = [
    'https://vk.com/album-113906974_268901626',
    'https://vk.com/album-113906974_269029261',
    'https://vk.com/album-113906974_268790663',
    'https://vk.com/album-113906974_268366883',
    'https://vk.com/album-113906974_268366647'
]

for album_url in album_urls:
    try:
        print(album_url)
        ids = re.search('album(.*)', album_url).group(1) # https://vk.com/znamenitye_zhenshiny?z=album-63418564_208781310

        owner_id = ids.split('_')[0]
        album_id = ids.split('_')[1]

        # название альбома
        # https://vk.com/dev/photos.getAlbums
        album_title = vk.photos.getAlbums(
          owner_id = owner_id, 
          album_ids = album_id
        )['items'][0]['title']

        fotos = vk.photos.get(
          owner_id = owner_id,
          album_id = album_id,
          count = 999
        )

        # создадим папку для альбома
        if not os.path.exists(home + album_title):
            os.mkdir(home + album_title, mode=0o777)           
            print('Folder __{}__ created'.format(home + album_title))
        else: 
            print('{} already exists'.format(home + album_title))
            continue

        for i in fotos['items']:

          try:
            foto_url = i['sizes'][-1]['url']

            # https://sun4-16.userapi.com/r9CRrpavGl8J1KPexPrFqLwuLDsgywBaNl7fJw/7KeyWyO6TZU.jpg
            foto_name = foto_url[60:].replace('/', '_')

            session = requests.Session()
            r = requests.get(foto_url, stream=True)
            image = r.raw.read()
            print(foto_url, album_title, sep='   ------   ')
            open(home + album_title + '/' + foto_name, "wb").write(image)
          
          except Exception as e:
              print(e)
              continue
        
    except Exception as e:
        print(e)
        continue
