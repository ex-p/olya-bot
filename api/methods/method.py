import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Method(object):
    def __init__(self, http, prefix):
        self._http = http
        self._prefix = prefix

    def _request(self, method_name, parameters):
        url = '{}.{}'.format(self._prefix, method_name)
        return self._http.request_method(url, params=parameters)

    @staticmethod
    def _process_response(response, cls=None):
        response.raise_for_status()
        logger.info('On request get response {}'.format(response.url, response.content))
        response = response.json()
        error = response.get('error')
        content = response.get('response')
        if error is None:
            if cls is None:
                return content, None
            return cls.from_dict(content), None
        return None, error
