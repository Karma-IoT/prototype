import peer

class KBucket:
    def __init__(self,prefix):
        self.prefix = prefix
        self.peers = {}
    
    def getK(self,K):
        return list(self.peers.values())[:K]
        
    def __len__(self):
        return len(self.peers)
        
    def get(self,addr):
        if addr in self.peers:
            return self.peers[addr]
        return None
        
    def append(self,p):
        self.peers[p.addr] = p
    
    def split(self):
        bucketR = KBucket(self.prefix + '1')
        self.prefix = self.prefix + '0'
        peers = self.peers
        self.peers = {}
        #print('---------------------')
        #print('left:',self.prefix,'right',bucketR.prefix)
        for _,x in peers.items():
            #print('{:0160b}'.format(int(x.addr,16))[:20],'     ',bucketR.prefix)
            if '{:0160b}'.format(int(x.addr,16))[:len(self.prefix)] == bucketR.prefix:
                bucketR.append(x)
                #print('right:',x.addr)
            else:
                #print('left:',x.addr)
                self.append(x)
        return bucketR
    
    @staticmethod
    def JSONEncode(obj):
        if isinstance(obj,KBucket):
            s = {}
            s['prefix'] = obj.prefix
            peers = []
            for _,x in obj.peers.items():
                peers.append(x)
            s['peers'] = peers
            s['_class'] = 'KBucket'
            return s
        else:
            return peer.Peer.JSONEncode(obj)
    
    @staticmethod
    def JSONDecode(o):
        if o['_class'] == 'KBucket':
            bucket =  KBucket(o['prefix'])
            for x in o['peers']:
                bucket.append(x)
            return bucket
        else:
            return peer.Peer.JSONDecode(o)

if __name__ == '__main__':
    import keystore
    import peer
    import json
    bucket = KBucket('')
    for x in range(20):
        d = keystore.Keystore()
        p = peer.Peer(d.addr,d.pk)
        bucket.append(p)
    print(len(bucket))
    s = json.dumps(bucket, indent = 4, default = KBucket.JSONEncode)
    #  print(s)
    #
    b = json.loads(s,object_hook = KBucket.JSONDecode)
    print(vars(b))
    #  p = json.dumps(bucket.getK(10),indent = 4,default = KBucketJSONEncode)
    #  print(p)
    
    #R = bucket.split()
    #print(json.dumps(bucket,indent = 4, default = KBucketJSONEncode))
    #print('---------------------------------------------------------')
    #print(json.dumps(R,indent = 4, default = KBucketJSONEncode))
    #print('---------------------------------------------------------')
    
    #R1 = R.split()
    #print(json.dumps(R,indent = 4, default = KBucketJSONEncode))
    #print('---------------------------------------------------------')
    #print(json.dumps(R1,indent = 4, default = KBucketJSONEncode))


