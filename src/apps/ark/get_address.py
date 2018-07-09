from apps.common import seed
from apps.common.display_address import show_address, show_qr
from trezor.messages.ArkAddress import ArkAddress

from .helpers import ARK_CURVE, get_address_from_public_key

async def ark_get_address(ctx, msg):
    address_n = msg.address_n or ()

    node = await seed.derive_node(ctx, address_n, ARK_CURVE)
    pubkey = node.public_key()
    pubkey = pubkey[1:]
    address = get_address_from_public_key(pubkey)

    if msg.show_display:
        while True:
            if await show_address(ctx, address):
                break
            if await show_qr(ctx, address):
                break

    return ArkAddress(address=address)
