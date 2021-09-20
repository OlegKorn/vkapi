import requests, os, re, time
import vk_api
import wget 
import logging


FORMAT = '%(message)s'

login = ""
passw = ""

owner_id = '-40368555' #'-63399807' #'-133382245' # '-33710306' # '-46985429' # '-78513317' # '-55407041'
# album_id = '265172957'
FORBIDEN_SYMBOLS = ('*,<>:\'\\"/\|?=')


class VkGroupAlbumsDownloader:
    def __init__(self):
        self.login = login
        self.passw = passw
      
        group_name=self.get_group_name()
        self.path = f'G:/Desktop/{group_name}/'
       
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


    def write_urls_album_title_and_foto_text_to_log(self):
        c = 0
        
        vk = self.vk_auth()
        albums = vk.photos.getAlbums(owner_id=owner_id)
        
        for album in albums['items']:
            fotos = vk.photos.get(
                owner_id = owner_id,
                album_id = album['id'],
                count = 999
            )
            album_title = album['title']

            # delete forbidden file name symbols
            for symbol in FORBIDEN_SYMBOLS:
                if symbol in album_title:
                    album_title = album_title.replace(symbol, ' ')
    
            for i in fotos['items']:
                url = i['sizes'][-1]['url']
                foto_title = i['text'].strip()

                if '\n' in foto_title:
                    foto_title = foto_title.replace('\n', '')

                # delete forbidden file name symbols
                for symbol in FORBIDEN_SYMBOLS:
                    if symbol in foto_title:
                        foto_title = foto_title.replace(symbol, ' ')
                            
                if len(foto_title) > 130:
                    foto_title = foto_title[0:129]

                # delete \n from url
                url_normalized = url.replace('\n', '').replace('&type=album', '').strip()
                url_normalized = re.search(r'.*(?<=&c_uniq_tag=)', url_normalized).group(0).replace('&c_uniq_tag=', '')

                logging.basicConfig(
                    filename=f"{self.path}urls.log",
                    level=logging.INFO, 
                    format=FORMAT
                )
                
                logging.info(f"{url_normalized}:::{album_title}:::{foto_title}")

                c += 1

                print(c, " - ", url_normalized)


    def download(self):
        c = 0

        urls = open(f"{self.path}urls.log").readlines()
        logging.basicConfig(
            filename=f"{self.path}downloaded.log",
            level=logging.INFO, 
            format=FORMAT
        )
                
        for i in urls:
            url = i.split(":::")[0].replace('\n', '')
            album = i.split(":::")[1].replace('\n', '')
            text = i.split(":::")[2].replace('\n', '')

            if text == '\n':
                text = ''

            try:
                session = requests.Session()
                r = requests.get(url.strip(), stream=True)
                image = r.raw.read()
                open(f"{self.path}{album}_{text}_{str(c)}.jpg", "wb").write(image)
                            
                logging.info(url)

                c += 1

                print(f"{c} - {album}_{text}_{str(c)}.jpg")
                        
            except Exception as e:
                print(f"{e}\n{url}\n")
                pass
        

v = VkGroupAlbumsDownloader()
# v.write_urls_album_title_and_foto_text_to_log()
v.download()





def _2ch_video(url):
    import requests
    from bs4 import BeautifulSoup as bs

    r = requests.get('https://2ch.hk/b/res/250161459.html', stream=True)
    
    print(r.text)
   












class VkUserAlbumsDownloader:

    owner_id = '349076567' # '243290837'  # '315315491' 400360145 307121640

    def __init__(self):
        self.login = login
        self.passw = passw
      
        self.path = f'G:/Desktop/vk_user_id{VkUserAlbumsDownloader.owner_id}/'
    
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


    def download_all(self, offset=None):
        vk = self.vk_auth()
        offset_ = None

        all_ = vk.photos.getAll(
            owner_id=VkUserAlbumsDownloader.owner_id,
            offset=offset
        ) 

        print(all_['count'])
        x = 0
        for i in all_['items']:
            print(i['sizes'][-1]['url'])
            print(x)
            x += 1


        '''

        urls = open(self.path + 'urls.txt', 'w')
        urls_downloaded = open(self.path + 'urls_downloaded.txt', 'w')

        for i in all_['items']:
            if all_['count'] <= 200:
                url = i['sizes'][-1]['url']

                try:
                    url_normalized = url.replace('\n', '').replace('&type=album', '').strip()
                    url_normalized_ = re.search(r'.*(?<=&c_uniq_tag=)', url_normalized).group(0).replace('&c_uniq_tag=', '')

                except Exception as e:
                    url_normalized_ = url_normalized

                try:
                    session = requests.Session()

                    # write urls into file
                    urls.write(url_normalized_)
                    urls.write('\n')

                    r = requests.get(url_normalized_, stream=True)

                    image = r.raw.read()
                    img_title_len = len(url_normalized_) - 12

                    print(self.path + (url_normalized_[img_title_len:].replace('/', '_')) + '.jpg')

                    open(self.path + '/' + url_normalized_[img_title_len:].replace('/', '_') + '.jpg', "wb").write(image)
                    urls_downloaded.write(url_normalized_)
                    urls_downloaded.write('\n')
                        
                except Exception as e:
                    print(f'{e}\nurl_normalized = {url_normalized}, \n')
                    break

        urls.close()
        urls_downloaded.close()
        '''
        

    def download_albums(self):
        vk = self.vk_auth()

        albums = vk.photos.getAlbums(owner_id=VkUserAlbumsDownloader.owner_id)
    
        urls = open(self.path + 'urls.txt', 'w')
        urls_downloaded = open(self.path + 'urls_downloaded.txt', 'w')
        
        for album in albums['items']:
            fotos = vk.photos.get(
                owner_id = VkUserAlbumsDownloader.owner_id,
                album_id = album['id'],
                count = 999
            )

            title = album['title'].replace('"', '').strip()

            album_path = self.path + title
            print(album_path)
            try:
                if not os.path.exists(album_path):
                    os.mkdir(album_path, mode=0o777)
                    print(f'Created path {album_path}')
                else:
                    print(f'Path {album_path} exists')
            except Exception as e:
                print(e)
                break

            print(title)
            
            for i in fotos['items']:
                # print(i['sizes'][-1]['url'])

                url = i['sizes'][-1]['url']
                # delete \n from url
                try:
                    url_normalized = url.replace('\n', '').replace('&type=album', '').strip()
                    url_normalized_ = re.search(r'.*(?<=&c_uniq_tag=)', url_normalized).group(0).replace('&c_uniq_tag=', '')

                except Exception as e:
                    url_normalized_ = url_normalized

                try:
                    session = requests.Session()

                    # write urls into file
                    urls.write(url_normalized_)
                    urls.write('\n')

                    r = requests.get(url_normalized_, stream=True)

                    image = r.raw.read()
                    img_title_len = len(url_normalized_) - 12

                    print(album_path + (url_normalized_[img_title_len:].replace('/', '_')) + '.jpg')

                    open(album_path + '/' + url_normalized_[img_title_len:].replace('/', '_') + '.jpg', "wb").write(image)
                    urls_downloaded.write(url_normalized_)
                    urls_downloaded.write('\n')
                    
                except Exception as e:
                    print(f'{e}, \n, url_normalized = {url_normalized}, \n')
                    continue
        
        urls.close()
        urls_downloaded.close()
