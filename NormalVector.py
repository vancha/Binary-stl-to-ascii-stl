'''
I have no idea what a normal vector is really, but it has some properties
'''
class NormalVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_ascii(self):
        return f"normal {self.x} {self.y} {self.z}"

