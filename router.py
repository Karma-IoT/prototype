class Router:
    def __init__(self):
        self.buckets = []
    
    def append(self,p):
        
        pass

    def get(self,addr):
        for x in self.buckets:
            if x.prefix == '{:0160b}'.format(int(addr,16))[:len(x.prefix)]:
                return x.get(addr)

    def getK(self,K):
        pass

    def __len__(self):
        pass



def RouterJSONEncode(obj):
    pass

def RouterJSONDecode(obj):
    pass
