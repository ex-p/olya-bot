import attr

from api.utils.tools import safe_index


@attr.s
class Update(object):
    code = attr.ib()

    @classmethod
    def from_dict(cls, data):
        code = data[0]
        if code == 4:
            message_update = MessageUpdate(code=code,
                                           message_id=data[1],
                                           flags=data[2],
                                           peer_id=safe_index(data, 3),
                                           timestamp=safe_index(data, 4),
                                           text=safe_index(data, 5),
                                           extra=safe_index(data, 6)
                                           )
        else:
            message_update = cls(code=code)
        return message_update


@attr.s
class MessageUpdate(Update):
    message_id = attr.ib()
    flags = attr.ib()
    peer_id = attr.ib(default=None)
    timestamp = attr.ib(default=None)
    subject = attr.ib(default=None)
    text = attr.ib(default=None)
    extra = attr.ib(default=None)

    def is_chat(self):
        return self.peer_id > 2000000000

    def chat_id(self):
        return self.peer_id - 2000000000

    def is_outbox(self):
        return self.flags & 2 == 2

    def sender(self):
        if self.is_chat():
            if self.extra:
                sender = self.extra.get('from', None)
                return int(sender) if sender else None
            return None
        return self.peer_id
