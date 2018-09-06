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
        bucketR = KBucket(self.prefix + '1')
        self.prefix = self.prefix + '0'
        peers = self.peers
        self.peers = []
        print('---------------------')
        print('left:',self.prefix,'right',bucketR.prefix)
        for x in peers:
            print('{:0160b}'.format(int(x.addr,16))[:20],'     ',bucketR.prefix)
            if '{:0160b}'.format(int(x.addr,16))[:len(self.prefix)] == bucketR.prefix:
                bucketR.append(x)
                print('right:',x.addr)
            else:
                print('left:',x.addr)
                self.peers.append(x)
        return bucketR
                
def KBucketJSONEncode(obj):
    if isinstance(obj,KBucket):
        s = {}
        s['prefix'] = obj.prefix
        peers = []
        for x in obj.peers:
            peers.append(peer.PeerJSONEncode(x))
        s['peers'] = peers
        s['_class'] = 'KBucket'
        return s
    elif isinstance(obj,peer.Peer):
        return peer.PeerJSONEncode(obj)
    return obj
    
def KBucketJSONDecode(o):
    if o['_class'] == 'Peer':
        return peer.PeerJSONDecode(o)
    elif o['_class'] == 'KBucket':
        bucket =  KBucket(o['prefix'])
        bucket.peers = o['peers']
        return bucket

if __name__ == '__main__':
    import keystore
    import peer
    import json
    bucket = KBucket('')
    for x in range(20):
        d = keystore.Keystore()
        p = peer.Peer(d.data['addr'],d.data['pk'])
        bucket.append(p)
    print(len(bucket))
    #  s = json.dumps(bucket, indent = 4, default = KBucketJSONEncode)
    #  print(s)
    #
    #  b = json.loads(s,object_hook = KBucketJSONDecode)
    #  print(vars(b))
    #  p = json.dumps(bucket.getK(10),indent = 4,default = KBucketJSONEncode)
    #  print(p)
    
    R = bucket.split()
    print(json.dumps(bucket,indent = 4, default = KBucketJSONEncode))
    print('---------------------------------------------------------')
    print(json.dumps(R,indent = 4, default = KBucketJSONEncode))
    print('---------------------------------------------------------')
    
    R1 = R.split()
    print(json.dumps(R,indent = 4, default = KBucketJSONEncode))
    print('---------------------------------------------------------')
    print(json.dumps(R1,indent = 4, default = KBucketJSONEncode))


