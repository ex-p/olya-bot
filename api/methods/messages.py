import logging

import requests

from api.methods.method import Method
from api.models.messages import LongPollServer
from api.models.updates import Update

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Messages(Method):
    def __init__(self, http):
        super(Messages, self).__init__(http, 'messages')

    def send(self, peer_id, message=None, *attachments, version='5.87'):
        method_name = 'send'
        params = {
            'peer_id': peer_id,
            'v': version,
        }
        if message:
            params['message'] = message
        attachments = ','.join(a.to_string() for a in attachments)
        if attachments:
            params['attachment'] = attachments
        return self._request(method_name, params)

    def get_long_poll_server(self, need_pts=False, version='5.87'):
        method_name = 'getLongPollServer'
        params = {
            'need_pts': int(need_pts),
            'v': version,
        }
        response = self._request(method_name, params)
        return self._process_response(response, LongPollServer)

    @staticmethod
    def get_long_poll_update(long_poll_server, mode=0):
        params = long_poll_server.to_dict()
        params.update({
            'act': 'a_check',
            'wait': 25,
            'mode': mode,
            'version': 2
        })
        url = 'https://{}'.format(long_poll_server.server)
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info('long poll update: {}'.format(data))
        return data['ts'], [Update.from_dict(u) for u in data['updates']]
