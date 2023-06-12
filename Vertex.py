''' 
Every vertex consists of three points, describing it's x, y and z location in 3d space
'''
class Vertex: 
    def __init__(self, x, y, z): 
        self.x = x 
        self.y = y 
        self.z = z

    def from_bytes(byte_array):
        return Vertex(struct.unpack_from("<f",byte_array[0:4])[0], struct.unpack_from("<f",byte_array[4:8])[0], struct.unpack_from("<f",byte_array[8:12] )[0])

    def to_ascii(self):
        return f"vertex {self.x} {self.y} {self.z}"

