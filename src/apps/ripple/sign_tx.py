from apps.common import seed
from trezor.crypto import der
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha512
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.messages.RippleSignedTx import RippleSignedTx
from trezor.messages.RippleTxTypeRequest import RippleTxTypeRequest
from trezor.messages import MessageType
from trezor.wire import ProcessError
from .serialize import serialize
from . import helpers
from . import layout


async def sign_tx(ctx, msg: RippleSignTx):
    node = await seed.derive_node(ctx, msg.address_n)

    if msg.account != helpers.address_from_public_key(node.public_key()):
        raise ProcessError('Source address is not equal to the one derived from a public key')

    tx_type = await ctx.call(RippleTxTypeRequest(), MessageType.RipplePaymentTxType)

    tx = serialize(msg, tx_type, pubkey=node.public_key())
    to_sign = get_network_prefix() + tx

    check_fee(msg.fee)

    await layout.require_confirm_fee(ctx, msg.fee)
    await layout.require_confirm_tx(ctx, tx_type.destination, tx_type.amount)

    signature = ecdsa_sign(node.private_key(), first_half_of_sha512(to_sign))
    tx = serialize(msg, tx_type, pubkey=node.public_key(), signature=signature)
    return RippleSignedTx(signature, tx)


def check_fee(fee: int):
    if fee < helpers.MIN_FEE or fee > helpers.MAX_FEE:
        raise ProcessError('Fee must be in the range of 10 to 10,000 drops')


def get_network_prefix():
    """Network prefix is prepended before the transaction and public key is included"""
    return helpers.HASH_TX_SIGN.to_bytes(4, 'big')


def first_half_of_sha512(b):
    """First half of SHA512, which Ripple uses"""
    hash = sha512(b)
    return hash.digest()[:32]


def ecdsa_sign(private_key: bytes, digest: bytes) -> bytes:
    """Signs and encodes signature into DER format"""
    signature = secp256k1.sign(private_key, digest)
    sig_der = der.encode_seq((signature[1:33], signature[33:65]))
    return sig_der
