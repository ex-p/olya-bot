import attr


@attr.s
class LongPollServer(object):
    key = attr.ib()
    server = attr.ib()
    ts = attr.ib()
    pts = attr.ib(default=None)

    @classmethod
    def from_dict(cls, kwargs):
        return cls(**kwargs)

    def to_dict(self):
        return attr.asdict(self)


@attr.s
class Message(object):
    id = attr.ib(default=None)
    date = attr.ib(default=None)
    peer_id = attr.ib(default=None)
    from_id = attr.ib(default=None)
    text = attr.ib(default=None)
    random_id = attr.ib(default=None)
    ref = attr.ib(default=None)
    ref_source = attr.ib(default=None)
    attachments = attr.ib(default=None)
    important = attr.ib(default=None)
    geo = attr.ib(default=None)
    payload = attr.ib(default=None)
    fwd_messages = attr.ib(default=None)
    action = attr.ib(default=None)
    out = attr.ib(default=None)

    @classmethod
    def from_dict(cls, data):
        return cls(data.get('id'),
                   data.get('date'),
                   data.get('peer_id'),
                   data.get('from_id'),
                   data.get('text'),
                   data.get('random_id'),
                   data.get('ref'),
                   data.get('ref_source'),
                   data.get('attachments'),
                   data.get('important'),
                   data.get('geo'),
                   data.get('payload'),
                   data.get('fwd_messages'),
                   data.get('action'),
                   data.get('out'))

    def is_chat(self):
        return self.peer_id >= 2000000000
