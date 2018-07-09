import protobuf as p

class ArkPublicKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 236
    FIELDS = {
        1: ('public_key', p.BytesType, 0),
    }

    def __init__(
        self,
        public_key: bytes = None,
    ) -> None:
        self.public_key = public_key
