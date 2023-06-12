from struct import unpack
import struct
EOF = -1
class stlReader:
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

    class Triangle:
        '''
            The Triangle consists of a surface normal (which can also calculated by taking the vector cross product of two edges of this triangle), and an array of exactyl 3 vertices/edges.
        '''
        def __init__(self, normal_vector, vertex_array):
            self.normal_vector = normal_vector
            self.vertices = vertex_array

        def to_ascii(self):
            return f"facet {self.normal_vector.to_ascii()}\n    outer loop\n        {self.vertices[0].to_ascii()}\n        {self.vertices[1].to_ascii()}\n        {self.vertices[2].to_ascii()}\n    endloop\nendfacet"


    def __init__(self, filename):
        if self.is_binary_stl(filename):
            self.read_binary_stl(filename)
        else:
            self.read_ascii_stl(filename)
        
        with open(filename, 'rb') as file:
            self.Header = file.read(80)
            self.number_of_triangles = file.read(4)


    def is_binary_stl(self, filename):
        with open(filename,'rb') as stl_file:
             return not b'solid' in stl_file.read(80)

    def read_binary_stl(self, filename):
        with open(filename, 'rb') as stl_file:
            self.Header = stl_file.read(80)
            self.number_of_triangles =  struct.unpack_from("<L",stl_file.read(4))[0]#stl_file.read(4)#this is probably in the wrong format(it´s little endian unsigned integer)
            self.data = []
            while True:
                try:
                    normal_vector               = stl_file.read(12)
                    vertex_1                    = stl_file.read(12)
                    vertex_2                    = stl_file.read(12)
                    vertex_3                    = stl_file.read(12)
                    attribute_byte_count        = stl_file.read(2)
                    if EOF not in [normal_vector, vertex_1, vertex_2, vertex_3,attribute_byte_count]:
                        normal_vector = self.NormalVector(struct.unpack_from("<f",normal_vector[0:4]),struct.unpack_from("<f",normal_vector[4:8]),struct.unpack_from("<f",normal_vector[8:12]))
                        vertex_v1   = self.Vertex(struct.unpack_from("<f",vertex_1[0:4]), struct.unpack_from("<f",vertex_1[4:8]), struct.unpack_from("<f",vertex_1[8:12]))
                        vertex_v2   = self.Vertex(struct.unpack_from("<f",vertex_2[0:4]), struct.unpack_from("<f",vertex_2[4:8]), struct.unpack_from("<f",vertex_2[8:12]))
                        vertex_v3   = self.Vertex(struct.unpack_from("<f",vertex_3[0:4]), struct.unpack_from("<f",vertex_3[4:8]), struct.unpack_from("<f",vertex_3[8:12]))
                        self.data.append(self.Triangle(normal_vector, [vertex_v1, vertex_v2, vertex_v3]))
                    else:
                        print('found eof')
                        break
                except Exception as e:
                    print(f'reached end of file probably: {str(e)}')
                    break
    
    def export_as_stl_ascii(self, destination_filename):
        #Solid name
        
        #facet normal n1 n2 n3
        #    outer loop
        #        vertex v11, v12, v13
        #        vertex v21, v22, v23
        #        vertex v31, v32, v33
        #    endloop 
        #endsolid name
        print('exporting to stl ascii')

    def read_ascii_stl(self, filename):
        pass



file_location = '/home/vancha/Documenten/python/stl_reader/binary_example.stl'
ascii_file_location = '/home/vancha/Documenten/python/stl_reader/ascii_example.stl'


stlreader = stlReader(file_location)
print(f'header: {stlreader.Header}')
num_triangles = struct.unpack_from("<L",stlreader.number_of_triangles)[0]

print(f'vertices: {num_triangles}')

