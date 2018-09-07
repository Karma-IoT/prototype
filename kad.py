from aiocoap import *

class KadFindNode:
    def __init__(self,router):
        self.router = router

    async def request(self,target, K):
        r = router.get(target)
        if r != None:
            return r
        targets = router.getK(target,K)


