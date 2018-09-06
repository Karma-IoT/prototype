import nacl
import nacl.signing
import nacl.encoding
import hashlib

class Keystore:
    def __init__(self,diffcult = 5):
        while 1:
            sk = nacl.signing.SigningKey.generate()
            self.sk = sk.encode(encoder = nacl.encoding.HexEncoder).decode()
            self.pk = sk.verify_key.encode(encoder = nacl.encoding.HexEncoder).decode()
            addr = hashlib.blake2s(sk.verify_key.encode(),digest_size = 20)
            p = hashlib.blake2s(addr.digest(),digest_size = 20)
            self.addr = addr.hexdigest()
            self.diffcult = diffcult
            #  print('{:0160b}'.format(int.from_bytes(p.digest(),byteorder = 'big')))
            if '{:0160b}'.format(int.from_bytes(p.digest(),byteorder = 'big'))[:diffcult] == ('{:0'+ str(diffcult) +'b}').format(0):
                break
    def sign(self,data):
        sk = nacl.signing.SigningKey(self.sk,encoder = nacl.encoding.HexEncoder)
        sm = sk.sign(data)
        return sm.signature,sm.message

    def verify(self,data,signature):
        pk = nacl.signing.VerifyKey(self.pk,encoder = nacl.encoding.HexEncoder)
        try:
            return pk.verify(data,signature = signature)
        except nacl.exceptions.BadSignatureError as e:
            print(e)
            return False

def KeystoreJSONEncode(obj):
    if isinstance(obj,Keystore):
        s = {}
        s['sk'] = obj.sk
        s['pk'] = obj.pk
        s['addr'] = obj.addr
        s['diffcult'] = obj.diffcult
        s['_class'] = 'Keystore'
        return s
    else:
        return obj

def KeystoreJSONDecode(o):
    if o['_class'] == 'Keystore':
        keystore = Keystore()
        keystore.sk = o['sk']
        keystore.pk = o['pk']
        keystore.addr = o['addr']
        keystore.diffcult = o['diffcult']
        return router
    else:
        return o


            
if __name__ == '__main__':
    import json
    k1 = Keystore()
    print(json.dumps(k1,indent = 4, default = KeystoreJSONEncode))
