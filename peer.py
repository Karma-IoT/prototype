import json
import hashlib
import nacl
import nacl.signing
import nacl.encoding

def _alt_prefix(bin_value):
    length = 160
    while 1:
        if bin_value[:length + 2] == bin(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)[:length + 2]:
            print(bin_value[:length + 2])
            return length
        length = length - 1

class Peer:
    def __init__(self, addr, pubkey = '', boxkey = '', info = []):
        self.addr = addr
        self.pubkey = pubkey
        self.boxkey = boxkey
        self.info = info
        self.diffcult = _alt_prefix(bin(int(hashlib.blake2s(int(addr,16).to_bytes(20,'big'),digest_size = 20).hexdigest(),16)))

    def verify(self,data,signature):
        pk = nacl.signing.VerifyKey(self.data['pubkey'],encoder = nacl.encoding.HexEncoder)
        try:
            return pk.verify(data,signature = signature)
        except nacl.exceptions.BadSignatureError as e:
            print(e)
            return False



if __name__ == '__main__':
    data = json.load(open('./keystore.json','r'))
    peer = Peer(data['addr'],pubkey = data['pk'])
    print(json.dumps(peer))
