import sys

import struct
from struct import unpack

from Triangle import Triangle
from NormalVector import NormalVector
from Vertex import Vertex

EOF = -1
'''
class that lets you convert binary stl to ascii stl, not to be used directly
'''
class stlReader:
    '''
    initializes stlReader with an stl file, loads stl file data to self
    '''
    def __init__(self, filename):
        if self.is_binary_stl(filename):
            self.read_binary_stl(filename)
        else:
            self.read_ascii_stl(filename)
    
    '''
    checks if the string filename points to a binary stl file
    '''
    def is_binary_stl(self, filename):
        with open(filename,'rb') as stl_file:
             return not b'solid' in stl_file.read(80)
    
    '''
    reads the file pointed to by filename as a binary stl file
    sets the following values:

        self.header                 the first 80 bytes of the stl file pointed to by filename
        self.number_of_triangles    the total number of triangles from the stl file pointed to by filename
        self.data                   the array containing all number_of_triangles triangles from the stl file pointed to by filename
    '''
    def read_binary_stl(self, filename):
        with open(filename, 'rb') as stl_file:
            self.Header = stl_file.read(80)
            self.number_of_triangles =  struct.unpack_from("<L",stl_file.read(4))[0]
            self.data = []

            while True:
                try:
                    normal_vector               = stl_file.read(12)
                    vertex_1                    = stl_file.read(12)
                    vertex_2                    = stl_file.read(12)
                    vertex_3                    = stl_file.read(12)
                    attribute_byte_count        = stl_file.read(2)
                    #if EOF not in [normal_vector, vertex_1, vertex_2, vertex_3,attribute_byte_count]:
                    normal_vector = NormalVector(struct.unpack_from("<f",normal_vector[0:4])[0],struct.unpack_from("<f",normal_vector[4:8])[0],struct.unpack_from("<f",normal_vector[8:12])[0])
                    vertex_v1   = Vertex(struct.unpack_from("<f",vertex_1[0:4])[0], struct.unpack_from("<f",vertex_1[4:8])[0], struct.unpack_from("<f",vertex_1[8:12])[0])
                    vertex_v2   = Vertex(struct.unpack_from("<f",vertex_2[0:4])[0], struct.unpack_from("<f",vertex_2[4:8])[0], struct.unpack_from("<f",vertex_2[8:12])[0])
                    vertex_v3   = Vertex(struct.unpack_from("<f",vertex_3[0:4])[0], struct.unpack_from("<f",vertex_3[4:8])[0], struct.unpack_from("<f",vertex_3[8:12])[0])
                    self.data.append(Triangle(normal_vector, [vertex_v1, vertex_v2, vertex_v3]))
                except struct.error:
                    break
    '''
    An ASCII stl file is structured like this:

    #Solid name
    #facet normal n1 n2 n3
    #    outer loop
    #        vertex v11, v12, v13
    #        vertex v21, v22, v23
    #        vertex v31, v32, v33
    #    endloop
    #endsolid name

    this function exports the read file as an ascii stl file, useful for conversion of binary stl to ascii stl
    '''
    def export_as_stl_ascii(self, destination_filename):
        with open(destination_filename, "w") as exported_file:
            exported_file.write("solid \n")
            for triangle in self.data:
                exported_file.write(triangle.to_ascii())
            exported_file.write("endsolid \n")
    '''
    not implemented cause i'm lazy
    '''
    def read_ascii_stl(self, filename):
        pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit('call this file with two arguments:\n1:\tThe file to read\n2:\tThe file to export to')
    binary_file_location = sys.argv[1]#'/home/vancha/Documenten/python/stl_reader/binary_example.stl'
    ascii_file_location = sys.argv[2]#'/home/vancha/Documenten/python/stl_reader/ascii_example.stl'
    stlreader = stlReader( binary_file_location )
    stlreader.export_as_stl_ascii( ascii_file_location )
