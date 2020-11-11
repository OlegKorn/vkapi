import requests, os
import vk_api
from wget import download


access_token = ''
api_version = '5.122'
owner_id = '-33710306'

home = 'G:/Pictures/катасонова/'
txt = 'G:/Pictures/Emma Watson/' + owner_id[1:] + '.txt' 
 

vk_session = vk_api.VkApi(
    'tel',
    "passw"
)

vk_session.auth()    
vk = vk_session.get_api()

group_name = vk.groups.getById(group_ids = owner_id.replace('-', ''))[0]['name'].replace(' ', '_')

if '|' in group_name:
    group_name = group_name.replace('|', '_')


'''
if not os.path.exists(home):
    os.mkdir(home, mode=0o777)           
    print('Folder __{}__ created'.format(home))
else: 
    print('{} already exists'.format(home))  
'''   


def main():

    f = open(txt, 'w')

    albums = vk.photos.getAlbums(owner_id = owner_id)['items']

    for _ in albums:
        # id of album
        album_id = _['id']
        album_title = _['title']

        if not ('2005' in album_title or '2004' in album_title or '2003' in album_title \
                or '2002' in album_title or '2001' in album_title or '2000' in album_title):
            print(f'downloading: {album_id}, {album_title}')

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


def get_all_fotos_of_user():

    owner_id = '33142641'
    home = f'G:/Pictures/id{owner_id}'
    get_all_fotos_of_user_txt = f'G:/Pictures/id{owner_id}/get_all_fotos_of_user.txt'

    if not os.path.exists(home):
        os.mkdir(home, mode=0o777)           
        print('Folder __{}__ created'.format(home))
    else: 
        print('{} already exists'.format(home)) 

    count = 200
    offset = 0

    f = open(get_all_fotos_of_user_txt, 'w')
    num_of_fotos = vk.photos.getAll(owner_id=owner_id, count=count)['count']

    while offset <= num_of_fotos:

        albums = vk.photos.getAll(owner_id=owner_id, count=count, offset=offset)['items']

        print('===============================')
        print(f'offset={offset}, num_of_fotos={num_of_fotos}, num_of_fotos-offset={num_of_fotos-offset}')
        print('===============================\n\n')
        
        for _ in albums:
            foto_url = _['sizes'][-1]['url']
            f.write(foto_url + '\n')
            print(foto_url)

        offset += 200

    f.close()


# get_all_fotos_of_user()


def save_img():
    owner_id = '33142641'
    home = f'G:/Pictures/id{owner_id}'
    get_all_fotos_of_user_txt = f'G:/Pictures/id{owner_id}/get_all_fotos_of_user.txt'

    f = open(get_all_fotos_of_user_txt, 'r').readlines()

    try:
        for url in f:
            print(url.strip())
            '''
            session = requests.Session()

            # delete \n from url
            url_normalized = url.replace('\n', '').strip()
            print(url_normalized)

            r = requests.get(url_normalized, stream=True)

            image = r.raw.read()
            img_title_len = len(url_normalized) - 12
            open(home + url_normalized[img_title_len:].replace('/', '_'), "wb").write(image)
            '''
            download(url.strip(), home)

        f.close()

    except Exception:
        pass


# main()
save_img()
