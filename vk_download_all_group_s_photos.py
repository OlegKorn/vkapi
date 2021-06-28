import requests, os, re, time
import vk_api
import wget 


login = ''
passw = ""

owner_id = '-46985429' # '-78513317' # '-55407041'
# album_id = '265172957'


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


    def download(self):
        vk = self.vk_auth()

        albums = vk.photos.getAlbums(owner_id=owner_id)

        urls = open(self.path + 'urls.txt', 'w')
        urls_downloaded = open(self.path + 'urls_downloaded.txt', 'w')

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
                # delete \n from url
                url_normalized = url.replace('\n', '').replace('&type=album', '').strip()
                url_normalized = re.search(r'.*(?<=&c_uniq_tag=)', url_normalized).group(0).replace('&c_uniq_tag=', '')
                
                try:
                    session = requests.Session()

                    # write urls into file
                    urls.write(url_normalized)
                    urls.write('\n')

                    r = requests.get(url_normalized, stream=True)

                    image = r.raw.read()
                    img_title_len = len(url_normalized) - 12

                    print(f'{self.path + title}' + '/' + (url_normalized[img_title_len:].replace('/', '_')) + '.jpg')

                    if not os.path.exists(f'{self.path + title}'):
                        os.mkdir(f'{self.path + title}', mode=0o777)
                        print(f'Created path {self.path + title}')

                    open(f'{self.path + title}' + '/' + url_normalized[img_title_len:].replace('/', '_') + '.jpg', "wb").write(image)
                    urls_downloaded.write(url_normalized)
                    urls_downloaded.write('\n')
                    

                except Exception as e:
                    print(f'{e}, \n, url_normalized = {url_normalized}, \n')
                    continue

        urls.close()
        urls_downloaded.close()


v = VkGroupAlbumsDownloader()
v.download()




















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



# v = VkUserAlbumsDownloader()
# v.download_all()


'''
delete arr__;
// get all <a> of all <div id="post_message_...">
let posts = document.querySelectorAll('[id^="post_message_"] a')
arr__ = [];
for (let i = 0; i < posts.length; i++) {
    if (posts[i]['href'].includes('.jp')) {
        arr__.push(posts[i]["href"]);
    }
};
arr__;
'''

'''
def download():

    from bs4 import BeautifulSoup as bs


    path = 'G:/Desktop/vincentlittlehat/'
    txt = 'G:/Desktop/vincentlittlehat/hrefs.txt'
    txt2 = 'G:/Desktop/vincentlittlehat/imgs.txt'
    marker = ': "'

    f = open(txt, 'r')
    f2 = open(txt2, 'w')
    
    for i in f:
        z = i.split(marker)
        if '.jp' in z[1]:
            link = z[1].strip().replace('"', '')
            f2.write(link)
            f2.write('\n')

            name = link[-20:]

            print(link)
            
    f.close()
    f2.close()

    f2 = open(txt2, 'r')

    for i in f2:
        i = i.strip()
        name = i[-20:]
        r = requests.get(i, stream=True)
            
          
        # with open(r'G:/Desktop/vincentlittlehat/','wb') as f:
        #     shutil.copyfileobj(r.raw, f)
        #     time.sleep(1.5)
        #     shutil.copyfileobj(r.raw, f, 50000)
        
        image = r.raw.read()
        open(path + name, "wb").write(image)
        time.sleep(1)
    
    f2.close()      

download()
'''
