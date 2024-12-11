from rpc import RPCClient

server = RPCClient('127.0.0.1', 8000)

server.connect()

result = server.add(5, 6)

print(result)

server.disconnect()
