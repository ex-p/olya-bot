import logging

from django.conf import settings
from django.http import HttpResponse

logging.basicConfig(**{
    'format': '%(asctime)s %(levelname)s %(name)-15s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def callback(request):
    data_type = request.POST('type', None)
    if data_type is None:
        return HttpResponse('Not responding')
    logger.info(request.POST.lists())
    if data_type == 'confirmation':
        return settings.CONFIRMATION_CODE
    return HttpResponse('ok')


def index(request):
    return HttpResponse('Not responding')
