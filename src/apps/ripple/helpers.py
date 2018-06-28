from trezor.crypto import base58ripple
from trezor.crypto.hashlib import sha256
from trezor.crypto.hashlib import ripemd160
from micropython import const

HASH_TX_ID = 0x54584E00  # 'TXN'
HASH_TX_SIGN = const(0x53545800)  # 'STX'
HASH_TX_SIGN_TESTNET = 0x73747800  # 'stx'


def address_from_public_key(pubkey: bytes) -> str:
    """Extracts public key from an address

    Ripple address is in format:
    <1-byte ripple flag> <20-bytes account id> <4-bytes dSHA-256 checksum>

    - 1-byte flag is 0x00 which is 'r' (Ripple uses its own base58 alphabet)
    - 20-bytes account id is a ripemd160(sha256(pubkey))
    - checksum is first 4 bytes of double sha256(data)

    see https://developers.ripple.com/accounts.html#address-encoding
    """
    """Returns the Ripple address created using base58"""
    h = sha256(pubkey).digest()
    h = ripemd160(h).digest()

    address = bytearray()
    address.append(0x00)  # 'r'
    address.extend(h)
    return base58ripple.encode_check(bytes(address))


def decode_address(address: str):
    """Returns so called Account ID"""
    adr = base58ripple.decode_check(address)
    return adr[1:]
