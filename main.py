from for_ya_disk import YandexDisk
import requests

from pprint import pprint
import time
from tqdm import tqdm
import json

TOKEN_YD = ''
TOKEN_VK = ''
vk_name = 'begemot_korovin'
dir_name = str(input('Введите имя папки:'))


class Vk_user:

    def __init__(self, token):
        self.token = token

    def get_user_id(self, vk_name):
        token = TOKEN_VK
        URL = 'https://api.vk.com/method/users.get'
        params = {
            'user_ids': vk_name,
            'access_token': token,
            'extended': '1',
            'v': '5.131',
        }
        user_id = requests.get(URL, params=params).json()['response'][0]['id']
        return user_id

    def get_user_pfotos(self, user_id):
        json_list = []
        likes_url_dict = {}
        like_list = []
        URL = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': TOKEN_VK,
            'album_id': 'profile',
            'v': '5.131',
            'owner_id': user_id,
            'extended': '1'
        }
        data = requests.get(URL, params=params).json()['response']['items']
        for photo in data:
            likes = photo['likes']['count']
            date_photo = photo['date']
            size = photo['sizes'][-1]['type']
            photo_url = photo['sizes'][-1]['url']
            if f'{likes}.jpg' not in like_list:
                likes_url_dict[f'{likes}.jpg'] = photo_url
                json_list.append({'file_name': f' {likes}. jpg', 'size': size})
                like_list.append(f'{likes}.jpg')
            else:
                likes_url_dict[f'{likes} {date_photo}.jpg'] = photo_url
                json_list.append({'file_name': f'{likes}_{date_photo}. jpg', 'size': size})
        with open('photo_vk.json', 'w') as data_file:

            json.dump(json_list, data_file, indent=4)

        return likes_url_dict.items()


class YaUploader:
    def __init__(self, token):
        self.token = token

    def make_dir(self, dir_name):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = self.get_headers()
        params = {'path': dir_name}
        response = requests.put(files_url, headers=headers, params=params)
        return

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = f'https://cloud-api.yandex.net/v1/disk/resources/files/'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return pprint(response.json())

    def upload_url(self, qty_photo=int(input('Введите количество фото: '))):

        b = list(vk.get_user_pfotos(user_id))

        for i in tqdm(b):
            time.sleep(1)
        if qty_photo > len(b):
            print(f'Столько фото нет в альбоме, максимальное количество {len(b)}')
            return

        for i in range((len(b) - (len(b) - (qty_photo)))):
            filename = (f'{dir_name}/{b[i][0]}')
            url_file = b[i][1]
            files_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload/'
            headers = self.get_headers()
            params = {'path': filename, 'url': url_file}
            response = requests.post(files_url, headers=headers, params=params)
        pprint('Успешная загрузка')
        return


if __name__ == '__main__':
    vk = Vk_user(token=TOKEN_VK)
    user_id = vk.get_user_id(vk_name)
    vk.get_user_pfotos(user_id)
    ya = YaUploader(token=TOKEN_YD)
    ya.make_dir(dir_name)
    ya.upload_url()
    # ya.get_files_list()
