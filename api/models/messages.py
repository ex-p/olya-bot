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
