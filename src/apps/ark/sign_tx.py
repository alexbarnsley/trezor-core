import ustruct
from apps.common import seed
from trezor import wire
from trezor.crypto.curve import secp256k1
from trezor.crypto.hashlib import sha256
from trezor.messages import ArkTransactionType
from trezor.messages.ArkSignedTx import ArkSignedTx
from trezor.utils import HashWriter

from . import layout
from .helpers import ARK_CURVE, get_address_from_public_key

async def ark_sign_tx(ctx, msg):
    pubkey, seckey = await _get_keys(ctx, msg)
    transaction = _update_raw_tx(msg.transaction, pubkey)

    try:
        await _require_confirm_by_type(ctx, transaction)
    except AttributeError:
        raise wire.DataError('The transaction has invalid asset data field')

    await layout.require_confirm_fee(ctx, transaction.amount, transaction.fee)

    txbytes = _get_transaction_bytes(transaction)
    txhash = HashWriter(sha256)
    for field in txbytes:
        txhash.extend(field)
    digest = txhash.get_digest()

    signature = secp256k1.sign(seckey, digest)

    return ArkSignedTx(signature=signature)

async def _get_keys(ctx, msg):
    address_n = msg.address_n or ()
    node = await seed.derive_node(ctx, address_n, ARK_CURVE)

    seckey = node.private_key()
    pubkey = node.public_key()
    # pubkey = pubkey[1:]  # skip ed25519 pubkey marker

    return pubkey, seckey

def _update_raw_tx(transaction, pubkey):
    transaction.sender_public_key = pubkey

    # For CastVotes transactions, recipientId should be equal to transaction
    # creator address.
    if transaction.type == ArkTransactionType.CastVotes:
        transaction.recipient_id = get_address_from_public_key(pubkey)

    return transaction

async def _require_confirm_by_type(ctx, transaction):

    if transaction.type == ArkTransactionType.Transfer:
        return await layout.require_confirm_tx(
            ctx, transaction.recipient_id, transaction.amount)

    if transaction.type == ArkTransactionType.RegisterDelegate:
        return await layout.require_confirm_delegate_registration(
            ctx, transaction.asset.delegate.username)

    if transaction.type == ArkTransactionType.CastVotes:
        return await layout.require_confirm_vote_tx(
            ctx, transaction.asset.votes)

    if transaction.type == ArkTransactionType.RegisterSecondPassphrase:
        return await layout.require_confirm_public_key(
            ctx, transaction.asset.signature.public_key)

    if transaction.type == ArkTransactionType.RegisterMultisignatureAccount:
        return await layout.require_confirm_multisig(
            ctx, transaction.asset.multisignature)

    raise wire.DataError('Invalid transaction type')

def _get_transaction_bytes(tx):

    # Required transaction parameters
    t_type = ustruct.pack('<b', tx.type)
    t_timestamp = ustruct.pack('<i', tx.timestamp)
    t_sender_public_key = tx.sender_public_key
    t_requester_public_key = tx.requester_public_key or b''

    if not tx.recipient_id:
        # Value can be empty string
        t_recipient_id = ustruct.pack('>Q', 0)
    else:
        # Ark uses big-endian for recipient_id, string -> int -> bytes
        t_recipient_id = ustruct.pack('>Q', int(tx.recipient_id[:-1]))

    t_amount = ustruct.pack('<Q', tx.amount)
    t_asset = _get_asset_data_bytes(tx)
    t_signature = tx.signature or b''

    return (t_type, t_timestamp, t_sender_public_key, t_requester_public_key,
            t_recipient_id, t_amount, t_asset, t_signature)

def _get_asset_data_bytes(msg):

    if msg.type == ArkTransactionType.Transfer:
        # Transfer transaction have optional data field
        if msg.asset.data is not None:
            return bytes(msg.asset.data, 'utf8')
        else:
            return b''

    if msg.type == ArkTransactionType.RegisterDelegate:
        return bytes(msg.asset.delegate.username, 'utf8')

    if msg.type == ArkTransactionType.CastVotes:
        return bytes(''.join(msg.asset.votes), 'utf8')

    if msg.type == ArkTransactionType.RegisterSecondPassphrase:
        return msg.asset.signature.public_key

    if msg.type == ArkTransactionType.RegisterMultisignatureAccount:
        data = b''
        data += ustruct.pack('<b', msg.asset.multisignature.min)
        data += ustruct.pack('<b', msg.asset.multisignature.life_time)
        data += bytes(''.join(msg.asset.multisignature.keys_group), 'utf8')
        return data

    raise wire.DataError('Invalid transaction type')
