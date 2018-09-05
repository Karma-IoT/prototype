import nacl
import nacl.signing
import nacl.encoding
import json
import os.path
import hashlib

class Keystore:
    def __init__(self,path = '',diffcult = 5):
        if path == '':
            self.path = './keystore.json'
            data = {}
            while 1:
                sk = nacl.signing.SigningKey.generate()
                data['sk'] = sk.encode(encoder = nacl.encoding.HexEncoder).decode()
                data['pk'] = sk.verify_key.encode(encoder = nacl.encoding.HexEncoder).decode()
                addr = hashlib.blake2s(sk.verify_key.encode(),digest_size = 20)
                p = hashlib.blake2s(addr.digest(),digest_size = 20)
                data['addr'] = addr.hexdigest()
                data['diffcult'] = diffcult
                if bin(int.from_bytes(p.digest(),byteorder = 'big'))[:diffcult + 2] == bin(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)[:diffcult + 2] :
                    break
            self.data = data

        else:
            self.path = path
            self.data = json.load(open(path,'r'))
            
    def store(self):
        json.dump(self.data,open(self.path,'w+'))

    def sign(self,data):
        sk = nacl.signing.SigningKey(self.data['sk'],encoder = nacl.encoding.HexEncoder)
        sm = sk.sign(data)
        return sm.signature,sm.message

    def verify(self,data,signature):
        pk = nacl.signing.VerifyKey(self.data['pk'],encoder = nacl.encoding.HexEncoder)
        try:
            return pk.verify(data,signature = signature)
        except nacl.exceptions.BadSignatureError as e:
            print(e)
            return False



if __name__ == '__main__':
    k1 = Keystore()
    print(k1.data)
