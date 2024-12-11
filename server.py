def add(a, b):
    return  str(int(a)+int(b))

def sub(a, b):
    return str(int(a)-int(b))

from rpc import RPCServer

server = RPCServer()

server.registerMethod(add)
server.registerMethod(sub)

server.run()