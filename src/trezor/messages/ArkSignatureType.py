import protobuf as p

class ArkSignatureType(p.MessageType):
    FIELDS = {
        1: ('public_key', p.BytesType, 0),
    }

    def __init__(
        self,
        public_key: bytes = None,
    ) -> None:
        self.public_key = public_key
