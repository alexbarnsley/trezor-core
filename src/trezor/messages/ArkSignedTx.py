import protobuf as p

class ArkSignedTx(p.MessageType):
    MESSAGE_WIRE_TYPE = 234
    FIELDS = {
        1: ('signature', p.BytesType, 0),
    }

    def __init__(
        self,
        signature: bytes = None,
    ) -> None:
        self.signature = signature
