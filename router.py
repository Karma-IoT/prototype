import kbucket

def _alt_prefix(bin_value,prefix):
    length = len(prefix)
    while 1:
        if prefix[:length] == '{:0160b}'.format(int(bin_value,16))[:length]:
            return length
        length = length - 1

class Router:
    def __init__(self):
        self.buckets = {'':kbucket.KBucket('')}
    
    def append(self,p,K = 20):
        keys = list(self.buckets.keys())
        keys.sort(key = lambda x: _alt_prefix(p.addr,x), reverse = True)
        #print(keys,p.addr)
        r = keys[0]
        for x in keys:
            if x == '{:0160b}'.format(int(p.addr,16))[:len(x)]:
                r = x
                break
        kbucket = self.buckets[r]
        del self.buckets[r]
        kbucket.append(p)
        if len(kbucket) > K:
            nbucket = kbucket.split()
            self.buckets[nbucket.prefix] = nbucket
        self.buckets[kbucket.prefix] = kbucket

    def get(self,addr):
        if addr in self.buckets:
            return self.buckets[addr]
        return None

    def getK(self,addr,K = 20):
        keys = list(self.buckets.keys())
        keys.sort(key = lambda x: _alt_prefix(addr,x), reverse = True)
        result = []
        for r in keys:
            res = self.buckets[r].getK(K)
            result = result + res
            K = K - len(res)
            if K <= 0:
                break
        return result

    def __len__(self):
        l = 0
        for x in self.buckets.values():
            l = l + len(x)
        return l

    @staticmethod
    def JSONEncode(obj):
        if isinstance(obj,Router):
            s = {}
            buckets = []
            for x in obj.buckets.values():
                buckets.append(x)
            s['buckets'] = buckets
            s['_class'] = 'Router'
            return s
        else:
            return kbucket.KBucket.JSONEncode(obj)

    @staticmethod
    def JSONDecode(o):
        if o['_class'] == 'Router':
            router = Router()
            del router.buckets['']
            for x in o['buckets']:
                router.buckets[x.prefix] = x
            return router
        else:
            return kbucket.KBucket.JSONDecode(o)
        
if __name__ == '__main__':
    import keystore
    import peer
    import json
    router = Router()
    ad = ''
    for x in range(50):
        d = keystore.Keystore()
        p = peer.Peer(d.addr,d.pk)
        router.append(p)
        ad = d.addr
    print(len(router))
    s = json.dumps(router,indent = 4, default = Router.JSONEncode)
    print(s)
    b20 = router.getK(ad)
    print(json.dumps(b20,indent = 4, default = Router.JSONEncode))
    print(ad)
    
