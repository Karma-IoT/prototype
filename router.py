import kbucket

class Router:
    def __init__(self):
        self.buckets = {'':kbucket.KBucket('')}
    
    def append(self,p,K = 20):
        keys = list(self.buckets.keys())
        keys.sort(key = lambda x: len(x), reverse = True)
        r = ''
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
        keys.sort(key = lambda x: len(x), reverse = True)
        lkeys = []
        for x in keys:
            lkeys.append(x)
            if x == '{:0160b}'.format(int(addr,16))[:len(x)]:
                break
        rkeys = keys[len(lkeys):]
        middle = lkeys.pop()
        R = [middle] + rkeys + lkeys
        print(R)
        result = []
        for r in R:
            res = self.buckets[r].getK(K)
            result = result + res
            K = K - len(res)
            if K <= 0:
                break
        return result

    def __len__(self):
        l = 0
        for x in self.buckets.values():
            print(x)
            l = l + len(x)
        return l

def RouterJSONEncode(obj):
    if isinstance(obj,Router):
        s = {}
        buckets = []
        for x in obj.buckets.values():
            buckets.append(x)
        s['buckets'] = buckets
        s['_class'] = 'Router'
        return s
    else:
        return kbucket.KBucketJSONEncode(obj)

def RouterJSONDecode(o):
    if o['_class'] == 'Router':
        router = Router()
        del router.buckets['']
        for x in o['buckets']:
            router.buckets[x.prefix] = x
        return router
    else:
        return kbucket.KBucketJSONDecode(o)
        
if __name__ == '__main__':
    import keystore
    import peer
    import json
    router = Router()
    ad = ''
    for x in range(50):
        d = keystore.Keystore()
        p = peer.Peer(d.data['addr'],d.data['pk'])
        router.append(p)
        ad = d.data['addr']
    print(len(router))
    s = json.dumps(router,indent = 4, default = RouterJSONEncode)
    print(s)
    b20 = router.getK(ad)
    print(json.dumps(b20,indent = 4, default = RouterJSONEncode))
    print(ad)
    
