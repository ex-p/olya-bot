from api.methods.messages import Messages
from api.utils.http import Http


class VkApi(object):
    def __init__(self, access_token):
        self._access_token = access_token
        self._http = Http(access_token)
        self._messages = Messages(self._http)

    @property
    def messages(self):
        return self._messages

    @property
    def http(self):
        return self._http
