import json
import logging

from django.conf import settings
from django.http import HttpResponse

from api.models.updates import Update, Confirmation, MessageNew
from api.vk import VkApi
from olya.logic import User

logging.basicConfig(**{
    'format': '%(asctime)s %(levelname)s %(name)-15s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
vk_api: VkApi = settings.VK_API


def handle_update(user, message):
    if message.is_chat():
        pass
    else:
        vk_api.messages.send(peer_id=message.peer_id, message=message.text)


def callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logging.info(data)
        update = Update.from_dict(data)
        logger.info(update)
        if isinstance(update, Confirmation):
            return HttpResponse(settings.CONFIRMATION_CODE)

        if isinstance(update, MessageNew):
            user_id = update.message.from_id
            if user_id is not None:
                user = settings.USERS.find_one({'user_id': user_id})
                if user is None:
                    user = User(user_id)
                else:
                    user = User.from_dict(user)

                handle_update(user, update.message)

                settings.USERS.replace_one({'user_id': user_id}, user.to_dict(), upsert=True)

    return HttpResponse('ok')


def index(request):
    return HttpResponse('Not responding')
