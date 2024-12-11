from rpc import RPCServer
from kps_image import ImageToKps

image_to_kps = ImageToKps()
def get_kps_all_faces(image_path):
    return image_to_kps.get_kps_all_faces(image_path)

# Run server
server = RPCServer()
server.registerMethod(get_kps_all_faces)
server.run()