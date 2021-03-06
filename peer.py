import hashlib
import nacl
import nacl.signing
import nacl.encoding

def _alt_prefix(bin_value):
    length = 160
    while 1:
        if bin_value[:length] == '{:0160b}'.format(0)[:length]:
            return length
        length = length - 1

class Peer:
    def __init__(self, addr, spk = '', epk = '', info = []):
        self.addr = addr
        self.spk = spk
        self.epk = epk
        self.info = info
        self.diffcult = _alt_prefix('{:0160b}'.format(int.from_bytes(hashlib.blake2s(int(addr,16).to_bytes(20,'big'),digest_size = 20).digest(),byteorder = 'big')))

    def verify(self,data,signature):
        pk = nacl.signing.VerifyKey(self.data['pubkey'],encoder = nacl.encoding.HexEncoder)
        try:
            return pk.verify(data,signature = signature)
        except nacl.exceptions.BadSignatureError as e:
            print(e)
            return False

    @staticmethod
    def JSONEncode(obj):
        if isinstance(obj,Peer):
            s = {}
            s['addr'] = obj.addr
            s['spk'] = obj.spk
            s['epk'] = obj.epk
            s['info'] = obj.info
            s['diffcult'] = obj.diffcult
            s['_class'] = 'Peer'
            return s
        else:
            return obj
        
    @staticmethod
    def JSONDecode(o):
        if o['_class'] == 'Peer':
            return Peer(o['addr'], o['spk'], o['epk'],o['info'])
        else:
            return o
        
    @staticmethod
    def CBOREncode(obj):
        if isinstance(obj,Peer):
            s = {}
            s[1] = int(obj.addr,16).to_bytes(20,'big')
            s[2] = int(obj.spk,16).to_bytes(32,'big')
            s[3] = obj.info
            return s
        return obj
    
    @staticmethod
    def CBORDecode(tag):
        return Peer(hex(int.from_bytes(tag[1],byteorder='big')), hex(int.from_bytes(tag[2],'big')),'',tag[3])
            
if __name__ == '__main__':
    import json
    import cbor2
    
    data = json.load(open('./keystore.json','r'))
    peer = Peer(data['addr'],spk = data['pk'],info = [1,'12345',2,'12435345'])
    s = json.dumps(peer, indent = 4, default = Peer.JSONEncode)
    print(s)
    b = json.loads(s,object_hook = Peer.JSONDecode)
    print(vars(b))

    s = cbor2.dumps(Peer.CBOREncode(peer))
    print(hex(int.from_bytes(s,byteorder='big')))
    b = Peer.CBORDecode(cbor2.loads(s))
    print(vars(b))
