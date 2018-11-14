import copy
import json
import logging
import queue
import threading

import attr

from api.models.updates import MessageUpdate
from api.vk import VkApi

logging.basicConfig(**{
    'format': '%(asctime)s %(levelname)s %(name)-15s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@attr.s
class KeyboardButton(object):
    text = attr.ib()
    label = attr.ib()
    color = attr.ib(default='Default')
    payload = attr.ib(default=attr.Factory(dict))

    COLOR_PRIMARY = 'Primary'
    COLOR_DEFAULT = 'Default'
    COLOR_NEGATIVE = 'Negative'
    COLOR_POSITIVE = 'Positive'

    def to_dict(self):
        return {
            'action': {
                'text': self.text,
                'label': self.label,
                'payload': json.dumps(self.payload)
            },
            'color': self.color
        }


def prepare_keyboard(buttons, one_time=False):
    buttons = copy.deepcopy(buttons)
    for i, row in enumerate(buttons):
        for j, button in enumerate(row):
            buttons[i][j] = button.to_dict()

    return {
        'one_time': one_time,
        'buttons': buttons
    }


def update_handler(messages: queue.Queue, vk_api: VkApi, is_chat):
    while True:
        try:

            long_poll_server, error = vk_api.messages.get_long_poll_server()
            if error is not None:
                return

            while True:
                ts, updates = vk_api.messages.get_long_poll_update(long_poll_server, 2)
                for update in updates:
                    if isinstance(update, MessageUpdate):
                        messages.put((is_chat, update))
                long_poll_server.ts = ts
        except Exception as e:
            logger.exception(e)


def message_handler(messages: queue.Queue, chat: VkApi, group: VkApi):
    while True:
        message: MessageUpdate
        is_chat, message = messages.get()
        logger.info('Message ({}): {}'.format(is_chat, message))
        if not message.is_outbox():
            if is_chat:
                pass
            else:
                buttons = [
                    [KeyboardButton(text='Ура!', label='ura', )]
                ]

                keyboard = {
                    'one_time': False,
                    'buttons': [[{
                        'action': {
                            'type': 'text',
                            'payload': json.dumps({'buttons': '1'}),
                            'label': 'Предыдущая',
                        },
                        'color': 'negative'
                    },
                        {
                            'action': {
                                'type': 'text',
                                'payload': json.dumps({'buttons': '2'}),
                                'label': 'Pred',
                            },
                            'color': 'primary'
                        }
                    ]]
                }
                keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
                keyboard = str(keyboard.decode('utf-8'))
                group.messages.send(peer_id=2000000001,
                                    message=message.text,
                                    keyboard=keyboard)

        messages.task_done()


def main():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    chat_bot = VkApi(access_token=secrets['chat'])
    group_bot = VkApi(access_token=secrets['group'])
    _, res = group_bot.messages.get_conversations()
    print(res)

    messages_pool = queue.Queue(maxsize=100)
    message_handler_thread = threading.Thread(target=message_handler,
                                              args=[messages_pool, chat_bot, group_bot])
    # chat_bot_update_thread = threading.Thread(target=update_handler, args=[messages_pool, chat_bot, True])
    group_bot_update_thread = threading.Thread(target=update_handler, args=[messages_pool, group_bot, False])
    message_handler_thread.start()
    # chat_bot_update_thread.start()
    group_bot_update_thread.start()

    while True:
        text = input()
        if text == 'quit':
            break


if __name__ == '__main__':
    main()
