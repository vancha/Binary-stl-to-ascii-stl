''' 
Every vertex consists of three points, describing it's x, y and z location in 3d space
'''
class Vertex: 
    def __init__(self, x, y, z): 
        self.x = x 
        self.y = y 
        self.z = z 

    def to_ascii(self):
        return f"vertex {self.x} {self.y} {self.z}"

