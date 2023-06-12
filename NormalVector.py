import struct

'''
I have no idea what a normal vector is really, but it has some properties
'''
class NormalVector:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def from_bytes(byte_array):
        return NormalVector(struct.unpack_from("<f",byte_array[0:4])[0],struct.unpack_from("<f",byte_array[4:8])[0],struct.unpack_from("<f",byte_array[8:12])[0])

    def to_ascii(self):
        return f"normal {self.x} {self.y} {self.z}"

