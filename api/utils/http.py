import requests


class Http(object):
    BASE_VK_API_URL = 'https://api.vk.com/method'

    def __init__(self, access_token):
        self._access_token = access_token

    def request_method(self, url, params=None):
        url = '{}/{}'.format(self.BASE_VK_API_URL, url)
        parameters = {'access_token': self._access_token}
        parameters.update(params)
        return requests.get(url, params=parameters)
