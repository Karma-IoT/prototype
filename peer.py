import json
import hashlib
import nacl
import nacl.signing
import nacl.encoding
import cbor2

def _alt_prefix(bin_value):
    length = 160
    while 1:
        if bin_value[:length + 2] == bin(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)[:length + 2]:
            return length
        length = length - 1

class Peer:
    def __init__(self, addr, spk = '', epk = '', info = []):
        self.addr = addr
        self.spk = spk
        self.epk = epk
        self.info = info
        self.diffcult = _alt_prefix(bin(int(hashlib.blake2s(int(addr,16).to_bytes(20,'big'),digest_size = 20).hexdigest(),16)))

    def verify(self,data,signature):
        pk = nacl.signing.VerifyKey(self.data['pubkey'],encoder = nacl.encoding.HexEncoder)
        try:
            return pk.verify(data,signature = signature)
        except nacl.exceptions.BadSignatureError as e:
            print(e)
            return False

def PeerJSONEncode(obj):
    if isinstance(obj,Peer):
        s = {}
        s['addr'] = obj.addr
        s['spk'] = obj.spk
        s['epk'] = obj.epk
        s['info'] = obj.info
        s['diffcult'] = obj.diffcult
        return s
    return obj
    
def PeerJSONDecode(o):
    return Peer(o['addr'], o['spk'], o['epk'],o['info'])
    
def PeerCBOREncode(obj):
    if isinstance(obj,Peer):
        s = {}
        s[1] = obj.addr
        s[2] = obj.spk
        s[3] = obj.info
        return s
    return obj
    
def PeerCBORDecode(tag):
    return Peer(tag[1], tag[2],'',tag[3])
        
if __name__ == '__main__':
    data = json.load(open('./keystore.json','r'))
    peer = Peer(data['addr'],spk = data['pk'],info = [1,'12345',2,'12435345'])
    s = json.dumps(peer, default = PeerJSONEncode)
    print(s)
    b = json.loads(s,object_hook = PeerJSONDecode)
    print(vars(b))

    s = cbor2.dumps(PeerCBOREncode(peer))
    print(s)
    b = PeerCBORDecode(cbor2.loads(s))
    print(vars(b))
