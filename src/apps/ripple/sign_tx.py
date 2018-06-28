from apps.common import seed
from trezor.crypto import der
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha512
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.messages.RippleSignedTx import RippleSignedTx
from trezor.messages.RippleTxTypeRequest import RippleTxTypeRequest
from trezor.messages.RipplePaymentTxType import RipplePaymentTxType
from trezor.messages.wire_types import RipplePaymentTxType
from .serialize import serialize_for_signing
from ubinascii import hexlify, unhexlify
from . import helpers


async def sign_tx(ctx, msg: RippleSignTx):
    node = await seed.derive_node(ctx, msg.address_n)

    tx_type = await ctx.call(RippleTxTypeRequest(), RipplePaymentTxType)

    s = unhexlify('902981cd5e0c862c53dc4854b6da4cc04179a2a524912d79800ac4c95435564d')
    p = unhexlify('02ae75b908f0a95f740a7bfa96057637e5c2170bc8dad13b2f7b52ae75faebefcf')
    tx = serialize_for_signing(msg, tx_type, p)

    signature = ecdsa_sign(s, first_half_of_sha512(tx))
    # print(hexlify(signature))

    return RippleSignedTx(signature)


def first_half_of_sha512(b):
    """First half of SHA512, which Ripple uses"""
    hash = sha512(b)
    return hash.digest()[:32]


def ecdsa_sign(private_key: bytes, digest: bytes) -> bytes:
    """Signs and encodes signature into DER format"""
    signature = secp256k1.sign(private_key, digest)
    # signature = ecdsa_make_canonical(signature[1:33], signature[33:65])
    sig_der = der.encode_seq((signature[1:33], signature[33:65]))
    return sig_der


# def ecdsa_make_canonical(r, s):
#     """Make sure the ECDSA signature is the canonical one.
#
#         https://github.com/ripple/ripple-lib/commit/9d6ccdcab1fc237dbcfae41fc9e0ca1d2b7565ca
#         https://ripple.com/wiki/Transaction_Malleability
#     """
#     # For a canonical signature we want the lower of two possible values for s
#     # 0 < s <= n/2
#     N = curves.SECP256k1.order # 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
#     if not N / 2 >= s:
#         s = N - s
#     return r, s
