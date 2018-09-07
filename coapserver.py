import asyncio
import aiocoap

from aiocoap import resource

class CoapServer:
    def __init__(self,bind = None):
        self.bind = bind
        self.root = resource.Site()

    def add(self,path,resource):
        self.root.add_resource(path,resource)

    def start(self):
        asyncio.Task(aiocoap.Context.create_server_context(self.root,bind = self.bind))
        asyncio.get_event_loop().run_forever()
        

if __name__ == "__main__":
    class TestResource(resource.Resource):
        def __init__(self):
            self.payload = b'test\n'
        
        async def render_get(self,request):
            print(request)
            return aiocoap.Message(payload = self.payload)

    server = CoapServer()
    server.add(('test',),TestResource())
    server.start()
