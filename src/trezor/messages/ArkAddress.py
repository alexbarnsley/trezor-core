import protobuf as p

class ArkAddress(p.MessageType):
    MESSAGE_WIRE_TYPE = 232
    FIELDS = {
        1: ('address', p.UnicodeType, 0),
    }

    def __init__(
        self,
        address: str = None,
    ) -> None:
        self.address = address
