from trezor.wire import register, protobuf_workflow
from trezor.messages.MessageType import ArkGetAddress, ArkGetPublicKey, ArkSignTx


def dispatch_ArkGetAddress(*args, **kwargs):
    from .get_address import ark_get_address
    return ark_get_address(*args, **kwargs)


def dispatch_ArkGetPublicKey(*args, **kwargs):
    from .get_public_key import ark_get_public_key
    return ark_get_public_key(*args, **kwargs)


def dispatch_ArkSignTx(*args, **kwargs):
    from .sign_tx import ark_sign_tx
    return ark_sign_tx(*args, **kwargs)


def boot():
    register(ArkGetAddress, protobuf_workflow, dispatch_ArkGetAddress)
    register(ArkGetPublicKey, protobuf_workflow, dispatch_ArkGetPublicKey)
    register(ArkSignTx, protobuf_workflow, dispatch_ArkSignTx)
