import requests, os, re, time
import vk_api
import wget 


login = ''
passw = ""

owner_id = '-29556'
# album_id = '265172957'


class VkGroupAlbumsDownloader:
    def __init__(self):
        self.login = login
        self.passw = passw
      
        group_name=self.get_group_name()
        self.path = f'G:/Desktop/py/{group_name}/'
       
        try:
            if not os.path.exists(self.path):
                os.mkdir(self.path, mode=0o777)
                print(f'Created path {self.path}')
            else:
                print(f'Path {self.path} exists')
        except Exception as e:
            print(f'Cant create path {self.path}')


    def vk_auth(self):        
        vk_session = vk_api.VkApi(self.login, self.passw)
        vk_session.auth()    
        vk = vk_session.get_api()

        return vk


    def get_group_name(self):
        vk = self.vk_auth()
        group_name = vk.groups.getById(group_ids = owner_id \
                              .replace('-', ''))[0]['name'] \
                              .replace(' ', '_') \
                              .replace('|', '-')

        return group_name


    def download(self):
        vk = self.vk_auth()

        albums = vk.photos.getAlbums(owner_id=owner_id)
        
        for album in albums['items']:
            print(album['title'])

            fotos = vk.photos.get(
                owner_id = owner_id,
                album_id = album['id'],
                count = 999
            )

            title = album['title'].replace('"', '')
            
            for i in fotos['items']:
                # print(i['sizes'][-1]['url'])

                url = i['sizes'][-1]['url']

                session = requests.Session()

                # delete \n from url
                url_normalized = url.replace('\n', '').replace('&type=album', '').strip()
                url_normalized = re.search(r'.*(?<=&c_uniq_tag=)', url_normalized).group(0).replace('&c_uniq_tag=', '')

                r = requests.get(url_normalized, stream=True)

                image = r.raw.read()
                img_title_len = len(url_normalized) - 12

                print(self.path + (url_normalized[img_title_len:].replace('/', '_')) + '.jpg')

                open(self.path + url_normalized[img_title_len:].replace('/', '_') + '.jpg', "wb").write(image)



v = VkGroupAlbumsDownloader()
v.download()
