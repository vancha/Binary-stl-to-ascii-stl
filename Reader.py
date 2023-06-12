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
        self.triangles              the array containing all number_of_triangles triangles from the stl file pointed to by filename
    '''
    def read_binary_stl(self, filename):

        with open(filename, 'rb') as stl_file:
            self.header                 = stl_file.read(80)
            self.number_of_triangles    = struct.unpack_from("<L",stl_file.read(4))[0]
            self.triangles              = []

            while True:
                try:
                    normal_vector           = NormalVector.from_bytes( stl_file.read(12) )
                    vertex_v1               = Vertex.from_bytes( stl_file.read(12) )
                    vertex_v2               = Vertex.from_bytes( stl_file.read(12) )
                    vertex_v3               = Vertex.from_bytes( stl_file.read(12) )
                    attribute_byte_count    = stl_file.read(2)

                    self.triangles.append( Triangle( normal_vector, [ vertex_v1, vertex_v2, vertex_v3 ] ))

                except struct.error:#this means we have read until the end of the binary file, we can likely safely break
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
    def export_as_ascii_stl(self, destination_filename):
        with open(destination_filename, "w") as exported_file:
            exported_file.write("solid \n")
            for triangle in self.triangles:
                exported_file.write(triangle.to_ascii())
            exported_file.write("endsolid \n")
    ''' 
    reads the file pointed to by filename as a ascii stl file
    sets the following values:

        self.header                 the first line of the stl file pointed to by filename
        self.triangles              the array containing all number_of_triangles triangles from the stl file pointed to by filename
    '''
    def read_ascii_stl(self, filename):
        with open(filename,'r') as stl_file:
            
            self.header = stl_file.readline()
            self.triangles = []
            
            while True:
                try:
                    _, _, x,y,z = stl_file.readline().strip().split(' ')#this line contains the normal
                    normal_vector = NormalVector(x,y,z)
                
                    _ = stl_file.readline()#ignore the next line, which has text `outer loop`
                
                    _, v1x, v1y, v1z = stl_file.readline().strip().split(' ')#get vertex 1 x, y and z
                    vertex_v1 = Vertex(v1x, v1y, v1z)
                
                    _, v2x, v2y, v2z = stl_file.readline().strip().split(' ')#get vertex 2 x, y and z
                    vertex_v2 = Vertex(v2x, v2y, v2z)
                
                    _, v3x, v3y, v3z = stl_file.readline().strip().split(' ')#get vertex 3 x, y and z
                    vertex_v3 = Vertex(v3x, v3y, v3z)
                
                    _ = stl_file.readline()#ignore the text `endloop`
                    _ = stl_file.readline()#ignore the text `endfacet`
                
                    self.triangles.append( Triangle(normal_vector, [vertex_v1, vertex_v2, vertex_v3] ) ) 
                except:
                    break


if __name__ == '__main__':
    if len(sys.argv) != 3:
        exit('\nCall this file with two arguments:\n1:\tThe file to read\n2:\tThe file to export to')
    
    binary_file_location    = sys.argv[1]
    ascii_file_location     = sys.argv[2]
    
    stlreader               = stlReader( binary_file_location )

    stlreader.export_as_ascii_stl( ascii_file_location )
