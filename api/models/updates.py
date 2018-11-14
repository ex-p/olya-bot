import attr

from api.models.messages import Message


@attr.s
class Update(object):
    raw = attr.ib()

    @classmethod
    def from_dict(cls, data):
        data_type = data['type']
        if data_type == 'confirmation':
            return Confirmation(raw=data, group_id=data['group_id'])
        if data_type == 'message_new':
            return MessageNew(raw=data, group_id=data['group_id'], message=Message.from_dict(data['object']))
        return cls(data)


@attr.s
class Confirmation(Update):
    group_id = attr.ib()


@attr.s
class MessageNew(Update):
    group_id = attr.ib()
    message: Message = attr.ib()
