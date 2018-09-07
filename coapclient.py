from aiocoap import *

class CoapClient:
    def __init__(self, peer):
        self.peer = peer
        self.remote = []
        for x in range(len(peer.info) / 2):
            endpoint = {}
            endpoint['type'] = peer.info[2 * x]
            if t == 1:
                arr = peer.info[2 * x + 1]
                endpoint['port'] = int.from_bytes(arr[0:1],'big')
                endpoint['addr'] = str(int.from_bytes(arr[2],'big')) + '.' + 
                                   str(int.from_bytes(arr[3],'big')) + '.' + 
                                   str(int.from_bytes(arr[4],'big')) + '.' + 
                                   str(int.from_bytes(arr[5],'big'))
            elif t == 2:
                arr = peer.info[2 * x + 1]
                endpoint['port'] = int.from_bytes(arr[0:1],'big')
                endpoint['addr'] = '{4x}'.format(arr[2:3],'big') + ':' +
                                   '{4x}'.format(arr[4:5],'big') + ':' +
                                   '{4x}'.format(arr[6:7],'big') + ':' +
                                   '{4x}'.format(arr[8:9],'big') + ':' +
                                   '{4x}'.format(arr[10:11],'big') + ':' +
                                   '{4x}'.format(arr[12:13],'big') + ':' +
                                   '{4x}'.format(arr[14:15],'big') + ':' +
                                   '{4x}'.format(arr[16:17],'big')
