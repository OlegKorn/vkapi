import requests, os
import vk_api


access_token = ''
api_version = '5.122'

owner_id = '-66666666666'

home = 'G:/Desktop/py/' + owner_id[1:] + '/'
txt = 'G:/Desktop/py/' + owner_id[1:] + '/' + owner_id[1:] + '.txt' 


def main():

    if not os.path.exists(home):
        os.mkdir(home, mode=0o777)           
        print('Folder __{}__ created'.format(home))
    else: 
        print('{} already exists'.format(home))

    f = open(txt, 'w')

    vk_session = vk_api.VkApi(
      num,
      pass
    )

    vk_session.auth()    
    vk = vk_session.get_api()

    wall_fotos = vk.photos.get(
        owner_id = owner_id, 
        album_id = 'wall'
    )['items']

    for _ in wall_fotos:
        foto_url = _['sizes'][-1]['url']
        print(foto_url)
        f.write(foto_url + '\n')

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


main()
save_img()
