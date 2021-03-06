import os.path
import json

class Manager:
    def __init__(self,path,cls,*args):
        self.path = path
        self.cls = cls
        if os.path.exists(path):
            # Load data
            self.ins = json.load(open(path,'r'),object_hook = cls.JSONDecode)
        else:
            # Create new
            self.ins = cls(*args)
            json.dump(self.ins,open(path,'w+'),indent = 4,default = cls.JSONEncode)
        
    def flush(self):
        json.dump(self.ins,open(self.path,'w'),indent = 4,default = self.cls.JSONEncode)

    def sync(self):
        self.ins = json.load(open(self.path,'r'),object_hook = self.cls.JSONDecode)



if __name__ == '__main__':
    import keystore
    manager = Manager('keystore.json',keystore.Keystore)
    print(type(manager.ins))

    import router
    import peer
    mrouter = Manager('router.json',router.Router)
    print(mrouter.ins)
    #  for x in range(10):
    #      d = keystore.Keystore()
    #      p = peer.Peer(d.addr,d.pk)
    #      mrouter.ins.append(p)
    print(len(mrouter.ins))
    #  mrouter.flush()
    print(json.dumps(mrouter.ins.get('0742a392bb79c31b49eceae267b37dbe399a7f9d'),indent = 4, default = mrouter.cls.JSONEncode))
    


