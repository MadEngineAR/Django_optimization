import requests
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from django.utils import timezone
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from social_core.exceptions import AuthException, AuthForbidden
from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(
                              OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_max_orig')),
                                          access_token=response['access_token'], v=5.131)), None))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    data_sex = {
        1: UserProfile.FEMALE,
        2: UserProfile.MALE,
        0: None
    }

    user.userprofile.gender = data_sex[data['sex']]
    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year

    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.age = age

    if data['photo_max_orig']:  # 2 часа серфа...В итоге догадался, что нужно сохранить скачанный из инета файл.
        r = requests.get(data['photo_max_orig'])
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()

        user.image.save("image.jpg", File(img_temp), save=True)
    user.save()
