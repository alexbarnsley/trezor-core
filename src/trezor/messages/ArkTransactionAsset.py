import protobuf as p
if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore
from .ArkDelegateType import ArkDelegateType
from .ArkMultisignatureType import ArkMultisignatureType
from .ArkSignatureType import ArkSignatureType

class ArkTransactionAsset(p.MessageType):
    FIELDS = {
        1: ('signature', ArkSignatureType, 0),
        2: ('delegate', ArkDelegateType, 0),
        3: ('votes', p.UnicodeType, p.FLAG_REPEATED),
        4: ('multisignature', ArkMultisignatureType, 0),
        5: ('data', p.UnicodeType, 0),
    }

    def __init__(
        self,
        signature: ArkSignatureType = None,
        delegate: ArkDelegateType = None,
        votes: List[str] = None,
        multisignature: ArkMultisignatureType = None,
        data: str = None,
    ) -> None:
        self.signature = signature
        self.delegate = delegate
        self.votes = votes if votes is not None else []
        self.multisignature = multisignature
        self.data = data
