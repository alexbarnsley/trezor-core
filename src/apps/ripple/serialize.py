# Serializes into the Ripple Format
#
# Inspired by https://github.com/miracle2k/ripple-python and https://github.com/ripple/ripple-lib
# Docs at https://wiki.ripple.com/Binary_Format and https://developers.ripple.com/transaction-common-fields.html
#
# The first four bits specify the field type (int16, int32, account..)
# the other four the record type (amount, fee, destination..) and then
# the actual data follow. This currently only supports the Payment
# transaction type and the fields that are required for it.
#
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.messages.RipplePaymentTxType import RipplePaymentTxType
from . import helpers

FIELD_TYPE_INT16 = 1
FIELD_TYPE_INT32 = 2
FIELD_TYPE_AMOUNT = 6
FIELD_TYPE_VL = 7
FIELD_TYPE_ACCOUNT = 8

FIELDS_MAP = {
    'account': FIELD_TYPE_ACCOUNT << 4 | 1,
    'amount': FIELD_TYPE_AMOUNT << 4 | 1,
    'destination': FIELD_TYPE_ACCOUNT << 4 | 3,
    'fee': FIELD_TYPE_AMOUNT << 4 | 8,
    'sequence': FIELD_TYPE_INT32 << 4 | 4,
    'type': FIELD_TYPE_INT16 << 4 | 2,
    'signingPubKey': FIELD_TYPE_VL << 4 | 3,
    'flags': FIELD_TYPE_INT32 << 4 | 2,
    'txnSignature': FIELD_TYPE_VL << 4 | 4,
}

TRANSACTION_TYPES = {
    'Payment': 0,
}

FLAG_FULLY_CANONICAL = 0x80000000


def serialize(common: RippleSignTx, tx_type: RipplePaymentTxType, pubkey=None, signature=None):
    w = bytearray()
    # must be sorted numerically first by type and then by name
    write(w, FIELDS_MAP['type'], TRANSACTION_TYPES['Payment'])
    write(w, FIELDS_MAP['flags'], common.flags)  # todo canonical flag??
    write(w, FIELDS_MAP['sequence'], common.sequence)
    write(w, FIELDS_MAP['amount'], tx_type.amount)
    write(w, FIELDS_MAP['fee'], common.fee)
    write(w, FIELDS_MAP['signingPubKey'], pubkey)
    write(w, FIELDS_MAP['txnSignature'], signature)
    write(w, FIELDS_MAP['account'], common.account)
    write(w, FIELDS_MAP['destination'], tx_type.destination)
    return w


def write(w: bytearray, field_type: int, value):
    if value is None:
        return
    w.append(field_type)
    field_type = field_type >> 4
    if field_type == FIELD_TYPE_INT16:
        w.extend(value.to_bytes(2, 'big'))
    elif field_type == FIELD_TYPE_INT32:
        w.extend(value.to_bytes(4, 'big'))
    elif field_type == FIELD_TYPE_AMOUNT:
        w.extend(serialize_amount(value))
    elif field_type == FIELD_TYPE_ACCOUNT:
        write_bytes(w, helpers.decode_address(value))
    elif field_type == FIELD_TYPE_VL:
        write_bytes(w, value)
    else:
        raise ValueError('Unknown field type')


def serialize_amount(value: int) -> bytearray:
    if value < 0 or isinstance(value, float):
        raise ValueError('Only positive integers are supported')
    if value > 100000000000:  # max allowed value
        raise ValueError('Value is larger than 100000000000')

    b = bytearray(value.to_bytes(8, 'big'))
    # Clear first bit to indicate XRP
    b[0] &= 0x7f
    # Set second bit to indicate positive number
    b[0] |= 0x40
    return b


def write_bytes(w: bytearray, value: bytes):
    """Serialize a variable length bytes."""
    serialize_varint(w, len(value))
    w.extend(value)


def serialize_varint(w, val):
    """https://ripple.com/wiki/Binary_Format#Variable_Length_Data_Encoding"""

    def rshift(val, n):
        # http://stackoverflow.com/a/5833119/15677
        return (val % 0x100000000) >> n

    assert val >= 0

    b = bytearray()
    if val < 192:
        b.append(val)
    elif val <= 12480:
        val -= 193
        b.extend([193 + rshift(val, 8), val & 0xff])
    elif val <= 918744:
        val -= 12481
        b.extend([
            241 + rshift(val, 16),
            rshift(val, 8) & 0xff,
            val & 0xff
        ])
    else:
        raise ValueError('Variable integer overflow.')

    w.extend(b)
