import json
import logging
import queue
import threading
import time

from api.models.updates import MessageUpdate
from api.vk import VkApi

logging.basicConfig(**{
    'format': '%(asctime)s %(levelname)s %(name)-15s %(message)s',
    'datefmt': '%Y-%m-%d %H:%M:%S'
})
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def update_handler(messages: queue.Queue, vk_api: VkApi):
    while True:
        try:

            long_poll_server, error = vk_api.messages.get_long_poll_server()
            if error is not None:
                return

            while True:
                ts, updates = vk_api.messages.get_long_poll_update(long_poll_server, 2)
                for update in updates:
                    if isinstance(update, MessageUpdate):
                        messages.put(update)
                long_poll_server.ts = ts
        except Exception as e:
            logger.exception(e)


def sender_handler(messages: queue.Queue, vk_api: VkApi):
    while True:
        message = messages.get()
        vk_api.messages.send(message.peer_id, message.text)
        time.sleep(1.0 / 29.0)
        messages.task_done()


def message_handler(messages: queue.Queue):
    while True:
        message = messages.get()
        if message is None:
            break
        if not message.is_outbox():
            pass
        messages.task_done()


def main():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)
    chat_bot = VkApi(access_token=secrets['chat'])
    group_bot = VkApi(access_token=secrets['group'])

    messages_pool = queue.Queue(maxsize=100)
    chat_bot_send_pool = queue.Queue(maxsize=100)
    group_bot_send_pool = queue.Queue(maxsize=100)
    message_handler_thread = threading.Thread(target=message_handler, args=[messages_pool])
    chat_bot_send_thread = threading.Thread(target=sender_handler, args=[chat_bot_send_pool, chat_bot])
    group_bot_send_thread = threading.Thread(target=sender_handler, args=[group_bot_send_pool, group_bot])
    chat_bot_update_thread = threading.Thread(target=update_handler, args=[messages_pool, chat_bot])
    group_bot_update_thread = threading.Thread(target=update_handler, args=[messages_pool, group_bot])
    message_handler_thread.start()
    chat_bot_send_thread.start()
    group_bot_send_thread.start()
    chat_bot_update_thread.start()
    group_bot_update_thread.start()

    while True:
        text = input()
        if text == 'quit':
            break


if __name__ == '__main__':
    main()
