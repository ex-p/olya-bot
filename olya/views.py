import json
import logging

from django.conf import settings
from django.http import HttpResponse

from api.models.updates import Update, Confirmation, MessageNew
from api.vk import VkApi

logging.basicConfig(**{
    'format': '%(asctime)s %(levelname)s %(name)-15s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
vk_api: VkApi = settings.VK_API


def callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logging.info(data)
        update = Update.from_dict(data)
        logger.info(update)
        if isinstance(update, Confirmation):
            return HttpResponse(settings.CONFIRMATION_CODE)

        if isinstance(update, MessageNew):
            vk_api.messages.send(peer_id=update.message.peer_id, message=update.message.text)
    return HttpResponse('ok')


def index(request):
    return HttpResponse('Not responding')
