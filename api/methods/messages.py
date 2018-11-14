import logging

from api.methods.method import Method
from api.models.messages import LongPollServer
from api.utils.tools import put_if_exist

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Messages(Method):
    def __init__(self, http):
        super(Messages, self).__init__(http, 'messages')

    def send(self,
             user_id=None,
             random_id=None,
             peer_id=None,
             domain=None,
             chat_id=None,
             user_ids=None,
             message=None,
             lat=None,
             long=None,
             attachment=None,
             forward_messages=None,
             sticker_id=None,
             group_id=None,
             keyboard=None,
             payload=None,
             dont_parse_links=None,
             version='5.87'):
        method_name = 'send'
        params = {'v': version}
        put_if_exist('user_id', user_id, params)
        put_if_exist('random_id', random_id, params)
        put_if_exist('peer_id', peer_id, params)
        put_if_exist('domain', domain, params)
        put_if_exist('chat_id', chat_id, params)
        put_if_exist('user_ids', user_ids, params)
        put_if_exist('message', message, params)
        put_if_exist('lat', lat, params)
        put_if_exist('long', long, params)
        put_if_exist('attachment', attachment, params)
        put_if_exist('forward_messages', forward_messages, params)
        put_if_exist('sticker_id', sticker_id, params)
        put_if_exist('group_id', group_id, params)
        put_if_exist('keyboard', keyboard, params)
        put_if_exist('payload', payload, params)
        put_if_exist('dont_parse_links', dont_parse_links, params)
        return self._process_response(self._request(method_name, params))

    def get_long_poll_server(self, need_pts=False, version='5.87'):
        method_name = 'getLongPollServer'
        params = {
            'need_pts': int(need_pts),
            'v': version,
        }
        response = self._request(method_name, params)
        return self._process_response(response, LongPollServer)

    def get_conversations(self, version='5.87'):
        method_name = 'getConversations'
        params = {'v': version}
        return self._process_response(self._request(method_name, params))
