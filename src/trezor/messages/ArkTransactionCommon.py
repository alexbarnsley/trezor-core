import protobuf as p
from .ArkTransactionAsset import ArkTransactionAsset


class ArkTransactionCommon(p.MessageType):
    FIELDS = {
        1: ('type', p.UVarintType, 0),
        2: ('amount', p.UVarintType, 0),  # default=0
        3: ('fee', p.UVarintType, 0),
        4: ('recipient_id', p.UnicodeType, 0),
        5: ('sender_public_key', p.BytesType, 0),
        6: ('requester_public_key', p.BytesType, 0),
        7: ('signature', p.BytesType, 0),
        8: ('timestamp', p.UVarintType, 0),
        9: ('asset', ArkTransactionAsset, 0),
    }

    def __init__(
        self,
        type: int = None,
        amount: int = None,
        fee: int = None,
        recipient_id: str = None,
        sender_public_key: bytes = None,
        requester_public_key: bytes = None,
        signature: bytes = None,
        timestamp: int = None,
        asset: ArkTransactionAsset = None,
    ) -> None:
        self.type = type
        self.amount = amount
        self.fee = fee
        self.recipient_id = recipient_id
        self.sender_public_key = sender_public_key
        self.requester_public_key = requester_public_key
        self.signature = signature
        self.timestamp = timestamp
        self.asset = asset
