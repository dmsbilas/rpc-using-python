from rpc import RPCClient
server = RPCClient('127.0.0.1', 8000)
server.connect()



image_path = "cup-1.jpeg"
output_path = "cup-1-kps.jpeg"
result = server.get_kps_all_faces(image_path)

print(result)

server.disconnect()
