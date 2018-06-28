from apps.common import seed
from trezor.crypto import der
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha512
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.messages.RippleSignedTx import RippleSignedTx
from trezor.messages.RippleTxTypeRequest import RippleTxTypeRequest
from trezor.messages import MessageType
from trezor.wire import ProcessError
from .serialize import serialize_for_signing
from . import helpers


async def sign_tx(ctx, msg: RippleSignTx):
    node = await seed.derive_node(ctx, msg.address_n)

    if msg.account != helpers.address_from_public_key(node.public_key()):
        raise ProcessError('Source address is not equal to the one derived from a public key')

    tx_type = await ctx.call(RippleTxTypeRequest(), MessageType.RipplePaymentTxType)
    tx = serialize_for_signing(msg, tx_type, node.public_key())

    signature = ecdsa_sign(node.private_key(), first_half_of_sha512(tx))
    return RippleSignedTx(signature)


def first_half_of_sha512(b):
    """First half of SHA512, which Ripple uses"""
    hash = sha512(b)
    return hash.digest()[:32]


def ecdsa_sign(private_key: bytes, digest: bytes) -> bytes:
    """Signs and encodes signature into DER format"""
    signature = secp256k1.sign(private_key, digest)
    sig_der = der.encode_seq((signature[1:33], signature[33:65]))
    return sig_der
