import attr


@attr.s
class User(object):
    user_id = attr.ib()
    conversation_id = attr.ib(default=None)

    def to_dict(self):
        return attr.asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
