import protobuf as p

class ArkDelegateType(p.MessageType):
    FIELDS = {
        1: ('username', p.UnicodeType, 0),
    }

    def __init__(
        self,
        username: str = None,
    ) -> None:
        self.username = username
