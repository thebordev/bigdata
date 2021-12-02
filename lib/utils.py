import requests
import json
import findCloneAPI

from config import YANDEX_IMG_URL, GOOGLE_IMG_URL


def get_url_yandex(filepath):
    files = {'upfile': ('blob', open(filepath, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(YANDEX_IMG_URL, params=params, files=files)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    img_search_url = YANDEX_IMG_URL + '?' + query_string
    return img_search_url


def get_url_google(filepath):
    multipart = {'encoded_image': (filepath, open(filepath, 'rb')), 'image_content': ''}
    response = requests.post(GOOGLE_IMG_URL, files=multipart, allow_redirects=False)
    img_search_url = response.headers['Location']
    return img_search_url


def get_info_findclone():
    file = '../me.jpg'
    find = findCloneAPI.FindCloneAPI()
    find.login()


if __name__ == '__main__':
    get_info_findclone()