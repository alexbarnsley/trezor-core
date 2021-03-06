# Automatically generated by pb2py
# fmt: off
import protobuf as p
from .HDNodeType import HDNodeType


class CardanoPublicKey(p.MessageType):
    MESSAGE_WIRE_TYPE = 306
    FIELDS = {
        1: ('xpub', p.UnicodeType, 0),
        2: ('node', HDNodeType, 0),
        3: ('root_hd_passphrase', p.UnicodeType, 0),
    }

    def __init__(
        self,
        xpub: str = None,
        node: HDNodeType = None,
        root_hd_passphrase: str = None,
    ) -> None:
        self.xpub = xpub
        self.node = node
        self.root_hd_passphrase = root_hd_passphrase
