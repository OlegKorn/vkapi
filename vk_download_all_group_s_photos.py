import requests, os
import vk_api


access_token = ''
api_version = '5.122'

# ex.: https://vk.com/club68046969 (owner_id = '-' + 68046969)
owner_id = '-68046969'

home = 'G:/Desktop/py/' + owner_id[1:] + '/'
txt = 'G:/Desktop/py/' + owner_id[1:] + '/' + owner_id[1:] + '.txt' 

if not os.path.exists(home):
    os.mkdir(home, mode=0o777)           
    print('Folder __{}__ created'.format(home))
else: 
    print('{} already exists'.format(home))



def main():
    f = open(txt, 'w')

    vk_session = vk_api.VkApi(
      'phone', 
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

        print('================')
        print(album_id)
        print('================')

        # grab all the fotos' urls from every album
        for foto in fotos['items']:
            foto_url = foto['sizes'][-1]['url']

            f.write(foto_url + '\n')
            print(foto_url)

    f.close()


def save_img():
    f = open(txt, 'r').readlines()

    try:
        for url in f:
            session = requests.Session()

            # delete \n from url
            url_normalized = url.replace('\n', '').strip()
            print(url_normalized)

            r = requests.get(url_normalized, stream=True)

            image = r.raw.read()
            img_title_len = len(url_normalized) - 12
            open(home + url_normalized[img_title_len:].replace('/', '_'), "wb").write(image)

        f.close()

    except Exception:
        pass

