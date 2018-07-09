import protobuf as p
if __debug__:
    try:
        from typing import List
    except ImportError:
        List = None  # type: ignore


class ArkMultisignatureType(p.MessageType):
    FIELDS = {
        1: ('min', p.UVarintType, 0),
        2: ('life_time', p.UVarintType, 0),
        3: ('keys_group', p.UnicodeType, p.FLAG_REPEATED),
    }

    def __init__(
        self,
        min: int = None,
        life_time: int = None,
        keys_group: List[str] = None,
    ) -> None:
        self.min = min
        self.life_time = life_time
        self.keys_group = keys_group if keys_group is not None else []