from common import *
# from apps.ripple.serializer import parse_non_native_amount
from apps.ripple.serializer import call_encoder
from apps.ripple.serializer import TypeSerializers
from apps.ripple.serializer import serialize_object


class TestRippleSerializer(unittest.TestCase):

    # def test_parse_amount(self):  todo
    #     """You don't really want to shift a zero here.
    #
    #     Match the output of:
    #
    #         function(s) {
    #             var a = Amount.from_human(s);
    #             return [a._is_negative, a._value.toString(), a._offset]
    #         }
    #     """
    #     p = parse_non_native_amount
    #     assert p('1') == (0, 1000000000000000, -15)
    #     assert p('-1') == (1, 1000000000000000, -15)
    #     assert p('9999') == (0, 9999000000000000, -12)
    #     assert p('0.1') == (0, 1000000000000000, -16)
    #     assert p('0.099') == (0, 9900000000000000, -17)
    #     assert p('1000.0001000') == (0, 1000000100000000, -12)
    #     assert p('1000.1000000') == (0, 1000100000000000, -12)
    #
    #     # This is special cased
    #     assert p('0') == (0, 0, -100)

    def test_amount(self):
        sa = call_encoder(TypeSerializers.STAmount)

        # XRP

        assert sa('0') == '4000000000000000'
        assert sa('1') == '4000000000000001'
        assert sa('-1') == '0000000000000001'
        with self.assertRaises(ValueError):
            sa('1.1')  # we could support floats, but don't for now

        # # Non-XRP
        #
        # assert sa({
        #     "value": "200000000",
        #     'issuer': 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV',
        #     'currency': 'USD'}) == \
        #        'D6871AFD498D00000000000000000000000000005553440000000000550FC62003E785DC231A1058A05E56E3F09CF4E6'
        #
        # assert sa({
        #     "value": "-21.00100",
        #     'issuer': 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV',
        #     'currency': 'USD'}) == \
        #        '94C77607A27E28000000000000000000000000005553440000000000550FC62003E785DC231A1058A05E56E3F09CF4E6'
        #
        # assert sa({
        #     "value": "0",
        #     'issuer': 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV',
        #     'currency': 'USD'}) == \
        #        '80000000000000000000000000000000000000005553440000000000550FC62003E785DC231A1058A05E56E3F09CF4E6'

    def test_vl_data(self):
        s = call_encoder(TypeSerializers.STVL)
        assert s('02AE75B908F0A95F740A7BFA96057637E5C2170BC8DAD13B2F7B52AE75FAEBEFCF') == \
               '2102AE75B908F0A95F740A7BFA96057637E5C2170BC8DAD13B2F7B52AE75FAEBEFCF'

    # def test_transactions(self):
    #     """Test some full transactions.
    #
    #     To get the reference output:
    #
    #         var SerializedObject = require('../src/js/ripple/serializedobject').SerializedObject;
    #         console.log(SerializedObject.from_json(tx_json).to_hex());
    #     """
    #
    #     def s(obj):
    #         return serialize_object(obj)
    #
    #     assert s({
    #         "TransactionType": "Payment",
    #         "Account": "r3P9vH81KBayazSTrQj6S25jW6kDb779Gi",
    #         "Destination": "r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV",
    #         "Amount": {"value": "200000000", 'issuer': 'r3kmLJN5D28dHuH8vZNUZpMC43pEHpaocV', 'currency': 'USD'},
    #         "Fee": "10",
    #         "Sequence": 1}) == \
    #            '120000240000000161D6871AFD498D00000000000000000000000000005553440000000000550FC62003E785DC231A1058A05E56E3F09CF4E668400000000000000A811450F97A072F1C4357F1AD84566A609479D927C9428314550FC62003E785DC231A1058A05E56E3F09CF4E6'


if __name__ == '__main__':
    unittest.main()
