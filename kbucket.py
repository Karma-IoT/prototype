import peer

class KBucket:
    def __init__(self,prefix):
        self.prefix = prefix
        self.peers = []
    
    def getK(self,K):
        return self.peers[:K]
        
    def __len__(self):
        return len(self.peers)
        
    def get(self,addr):
        for x in self.peers:
            if x.addr == addr:
                return x
        return None
        
    def append(self,p):
        self.peers.append(p)
    
    def split(self):
        bucketL = self
        prefix = bucketL.prefix
        bucketL.prefix = prefix + '0'
        bucketR = KBucket(prefix + '1')
        for x in bucketL.peers:
            if bin(int(x.addr,16))[:len(bucketL.prefix)] == bucketR.prefix:
                bucketL.remove(x)
                bucketR.append(x)
                
def KBucketJSONEncode(obj):
    if isinstance(obj,KBucket):
        s = {}
        s['prefix'] = obj.prefix
        peers = []
        for x in obj.peers:
            peers.append(peer.PeerJSONEncode(x))
        s['peers'] = peers
        return s
    return obj
    
def KBucketJSONDecode(o):
    print(o)
    #return KBucket(o['prefix'], o['spk'], o['epk'],o['info'])

if __name__ == '__main__':
    import keystore
    import peer
    import json
    bucket = KBucket('0b')
    for x in range(30):
        d = keystore.Keystore()
        p = peer.Peer(d.data['addr'],d.data['pk'])
        bucket.append(p)

    s = json.dumps(bucket, default = KBucketJSONEncode)
    #print(s)
    
    b = json.loads(s,object_hook = KBucketJSONDecode)
    #print(vars(b))
    
    
