from common import *
from apps.ripple.serialize import serialize
from apps.ripple.serialize import serialize_amount
from apps.ripple.serialize import serialize_for_signing
from trezor.messages.RippleSignTx import RippleSignTx
from trezor.messages.RipplePaymentTxType import RipplePaymentTxType


class TestRippleSerializer(unittest.TestCase):

    def test_amount(self):
        # https://github.com/ripple/ripple-binary-codec/blob/4581f1b41e712f545ba08be15e188a557c731ecf/test/fixtures/data-driven-tests.json#L2494
        assert serialize_amount(0) == unhexlify('4000000000000000')
        assert serialize_amount(1) == unhexlify('4000000000000001')
        assert serialize_amount(93493429243) == unhexlify('40000015c4a483fb')
        with self.assertRaises(ValueError):
            serialize_amount(1000000000000000000)  # too large
        with self.assertRaises(ValueError):
            serialize_amount(-1)  # negative not supported
        with self.assertRaises(ValueError):
            serialize_amount(1.1)  # float numbers not supported

    def test_transactions(self):
        # from https://github.com/miracle2k/ripple-python
        common = RippleSignTx(None, 'r3P9vH81KBayazSTrQj6S25jW6kDb779Gi', 10, None, 1, None)
        type = RipplePaymentTxType(200000000, 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV')
        assert serialize(common, type) == unhexlify('120000240000000161400000000bebc20068400000000000000a811450f97a072f1c4357f1ad84566a609479d927c9428314550fc62003e785dc231a1058a05e56e3f09cf4e6')

        common = RippleSignTx(None, 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV', 99, None, 99, None)
        type = RipplePaymentTxType(1, 'r3P9vH81KBayazSTrQj6S25jW6kDb779Gi')
        assert serialize(common, type) == unhexlify('12000024000000636140000000000000016840000000000000638114550fc62003e785dc231a1058a05e56e3f09cf4e6831450f97a072f1c4357f1ad84566a609479d927c942')

        # https://github.com/ripple/ripple-binary-codec/blob/4581f1b41e712f545ba08be15e188a557c731ecf/test/fixtures/data-driven-tests.json#L1579
        common = RippleSignTx(None, 'r9TeThyi5xiuUUrFjtPKZiHcDxs7K9H6Rb', 10, 0, 2)
        tx_type = RipplePaymentTxType(25000000, 'r4BPgS7DHebQiU31xWELvZawwSG2fSPJ7C')
        assert serialize(common, tx_type) == unhexlify('120000220000000024000000026140000000017d784068400000000000000a81145ccb151f6e9d603f394ae778acf10d3bece874f68314e851bbbe79e328e43d68f43445368133df5fba5a')

        # https://github.com/ripple/ripple-binary-codec/blob/4581f1b41e712f545ba08be15e188a557c731ecf/test/fixtures/data-driven-tests.json#L1651
        # common = RippleSignTx(None, 'rGWTUVmm1fB5QUjMYn8KfnyrFNgDiD9H9e', 15, 0, 144, 6220218)
        # tx_type = RipplePaymentTxType(200000, 'rw71Qs1UYQrSQ9hSgRohqNNQcyjCCfffkQ')
        # assert serialize(common, tx_type) == unhexlify('12000022000000002400000090201B005EE9BA614000000000030D4068400000000000000F8114AA1BD19D9E87BE8069FDBF6843653C43837C03C6831467FE6EC28E0464DD24FB2D62A492AAC697CFAD02')

        # https://github.com/ripple/ripple-binary-codec/blob/4581f1b41e712f545ba08be15e188a557c731ecf/test/fixtures/data-driven-tests.json#L1732
        # common = RippleSignTx(None, 'r4BPgS7DHebQiU31xWELvZawwSG2fSPJ7C', 12, 0, 1)
        # tx_type = RipplePaymentTxType(25000000, 'r4BPgS7DHebQiU31xWELvZawwSG2fSPJ7C', 4146942154)
        # assert serialize(common, tx_type) == unhexlify('120000220000000024000000012ef72d50ca6140000000017d784068400000000000000c8114e851bbbe79e328e43d68f43445368133df5fba5a831476dac5e814cd4aa74142c3ab45e69a900e637aa2')

    def test_transactions_with_pubkey(self):
        # https://github.com/ripple/ripple-binary-codec/blob/4581f1b41e712f545ba08be15e188a557c731ecf/test/signing-data-encoding-test.js
        common = RippleSignTx(None, 'r9LqNeG6qHxjeUocjvVki2XR35weJ9mZgQ', 10, 2147483648, 1)
        tx_type = RipplePaymentTxType(1000, 'rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh')
        blob = serialize_for_signing(common, tx_type, unhexlify('ed5f5ac8b98974a3ca843326d9b88cebd0560177b973ee0b149f782cfaa06dc66a'))
        assert blob[0:4] == unhexlify('53545800')  # signing prefix
        assert blob[4:7] == unhexlify('120000')  # transaction type
        assert blob[7:12] == unhexlify('2280000000')  # flags
        assert blob[12:17] == unhexlify('2400000001')  # sequence
        assert blob[17:26] == unhexlify('6140000000000003e8')  # amount
        assert blob[26:35] == unhexlify('68400000000000000a')  # fee
        assert blob[35:70] == unhexlify('7321ed5f5ac8b98974a3ca843326d9b88cebd0560177b973ee0b149f782cfaa06dc66a')  # singing pub key
        assert blob[70:92] == unhexlify('81145b812c9d57731e27a2da8b1830195f88ef32a3b6')  # account
        assert blob[92:114] == unhexlify('8314b5f762798a53d543a014caf8b297cff8f2f937e8')  # destination
        assert len(blob[114:]) == 0  # that's it


if __name__ == '__main__':
    unittest.main()
