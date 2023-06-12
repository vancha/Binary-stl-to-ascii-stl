class Triangle:
    ''' 
        The Triangle consists of a surface normal (which can also calculated by taking the vector cross product of two edges of this triangle), and an array of exactyl 3 vertices/edges.
    '''
    def __init__(self, normal_vector, vertex_array):
        self.normal_vector = normal_vector
        self.vertices = vertex_array

    def to_ascii(self):
        return f"facet {self.normal_vector.to_ascii()}\n    outer loop\n        {self.vertices[0].to_ascii()}\n        {self.vertices[1].to_ascii()}\n        {self.vertices[2].to_ascii()}\n    endloop\nendfacet\n"

